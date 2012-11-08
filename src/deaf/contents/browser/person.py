
from five import grok
from deaf.contents.browser.document import DocumentView
from deaf.contents.browser.utils import get_lead_image
from zeam.utils.batch import AlphabeticalBatch, IBatching
from zope.component import queryMultiAdapter

from deaf.contents.browser.document import DocumentActions

from Products.Person.interfaces import IPerson
from Products.ATContentTypes.interfaces.folder import IATFolder
from Products.CMFCore.utils import getToolByName


class PersonFolderView(grok.View):
    grok.context(IATFolder)
    grok.name('person_folder_view')

    def update(self):
        catalog = getToolByName(self.context, 'portal_catalog')

        def get_people(letter=None):
            query = dict(
                portal_type=('Person',),
                path='/'.join(self.context.getPhysicalPath()),
                sort_on='sortable_title',
                sort_order='ascending')
            if letter:
                query['Title'] = '%s*' % letter
            return catalog(**query)

        self.peoples = AlphabeticalBatch(
            get_people,
            request=self.request,
            factory=lambda b: b.getObject(),
            no_default=True)
        self.batch = queryMultiAdapter(
            (self.context, self.peoples, self.request),
            IBatching)


class PersonView(DocumentView):
    grok.context(IPerson)
    grok.name('person_view')


class PersonDetails(grok.Viewlet):
    grok.context(IPerson)
    grok.viewletmanager(DocumentActions)
    grok.order(20)

    def update(self):
        self.description = self.context.Description()


class PersonThumbnailView(grok.View):
    grok.context(IPerson)
    grok.name('thumbnail_view')

    def update(self):
        self.name = self.context.Title()
        self.url = self.context.absolute_url()
        self.photo = get_lead_image(self.context, size='mini')
