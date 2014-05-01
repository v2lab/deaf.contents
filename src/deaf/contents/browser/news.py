
from five import grok
from zeam.utils.batch import Batch, IBatching
from zope.component import queryMultiAdapter

from Products.ATContentTypes.interfaces.folder import IATFolder
from Products.ATContentTypes.interfaces.news import IATNewsItem
from Products.CMFCore.utils import getToolByName

from deaf.contents.browser.document import DocumentView
from deaf.contents.browser.document import DocumentActions, DocumentExtras
from deaf.contents.browser.utils import get_category, format_date


class NewsComposedFolderView(grok.View):
    grok.name('news_composed_folder_view')

    NEWS_COUNT = 5

    def update(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        path = '/'.join(self.context.getPhysicalPath())
        self.containers = []
        for subject in self.context.Subject()[:2]:
            items = Batch(
                catalog(
                    portal_type=('News Item',),
                    sort_on='effective',
                    sort_order='reverse',
                    Subject=subject,
                    path=path),
                factory=lambda b: b.getObject(),
                name=subject,
                count=self.NEWS_COUNT,
                request=self.request)
            self.containers.append(
                {'title': subject,
                 'news': items,
                 'batch': queryMultiAdapter(
                        (self.context, items, self.request), IBatching)()
                 })


class NewsItemView(DocumentView):
    grok.context(IATNewsItem)
    grok.name('newsitem_view')


class NewsItemExtra(grok.Viewlet):
    grok.context(IATNewsItem)
    grok.viewletmanager(DocumentExtras)
    grok.order(10)

    def available(self):
        return self.image_url is not None

    def update(self):
        self.image_url = None
        self.image_caption = None
        if self.context.getImage():
            self.image_url = self.view.url + '/image_preview'
            self.image_caption = self.context.getImageCaption()


class NewsItemDetails(grok.Viewlet):
    grok.context(IATNewsItem)
    grok.viewletmanager(DocumentActions)
    grok.order(20)

    def update(self):
        self.category = get_category(self.context)
        self.date = format_date(self.context.EffectiveDate())


class NewsItemMiniThumbnailView(grok.View):
    grok.context(IATNewsItem)
    grok.name('mini_thumbnail_view')

    def update(self):
        self.url = self.context.absolute_url()
        self.title = self.context.Title()
        self.description = self.context.Description()
        self.category = get_category(self.context)
        self.date = format_date(self.context.EffectiveDate())


class NewsItemThumbnailView(NewsItemMiniThumbnailView):
    grok.name('thumbnail_view')

    def update(self):
        super(NewsItemThumbnailView, self).update()
        self.date = format_date(self.context.EffectiveDate())
        self.image_url = None
        if self.context.getImage():
            self.image_url = self.url + '/image_panorama'
