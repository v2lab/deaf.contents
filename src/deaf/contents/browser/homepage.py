
from five import grok

from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from Products.CMFCore.utils import getToolByName


class HomePage(grok.View):
    grok.context(IPloneSiteRoot)
    grok.name('homepage_view')

    NEWS_COUNT = 7

    def update(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        self.news = map(
            lambda b: b.getObject(),
            catalog(
                portal_type=('News Item',),
                sort_on='effective',
                sort_order='reverse',
                sort_limit=self.NEWS_COUNT)[:self.NEWS_COUNT])

        self.slideshow = catalog(
            portal_type=('Image',),
            path=dict(
                query="/".join(self.context.getPhysicalPath() + ('slideshow',)),
                depth=1),
            sort_on='getObjPositionInParent')
