
import operator

from five import grok
from zope.component import getMultiAdapter
from deaf.contents.browser.document import DocumentView, DocumentExtras
from deaf.contents.browser.utils import get_lead_image

from Products.ATContentTypes.interfaces.folder import IATFolder
from Products.CMFCore.utils import getToolByName
from Products.Maps.interfaces import ILocation


class LocationFolderView(grok.View):
    grok.context(IATFolder)
    grok.name('location_folder_view')

    def update(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        index = self.context._getOb('index', None)
        if index is not None:
            self.index = index.getText()
        else:
            self.index = None
        self.locations = map(
            lambda b: b.getObject(),
            catalog(portal_type=('GeoLocation',),
                    path='/'.join(self.context.getPhysicalPath()),
                    sort_on='getObjPositionInParent',
                    sort_order='ascending'))

        def get_markers(location):
            view = getMultiAdapter(
                (location, self.request), name='maps_googlemaps_view')
            result = []
            for marker in view.getMarkers():
                result.append({'marker': marker,
                               'name': location.UID(),
                               'icon': view.iconTagForMarker(marker)})
            return result

        maps = map(get_markers, self.locations)
        if maps:
            maps = reduce(operator.add, maps)
        self.maps = maps


class LocationView(DocumentView):
    grok.context(ILocation)
    grok.name('location_view')


class LocationExtra(grok.Viewlet):
    grok.context(ILocation)
    grok.viewletmanager(DocumentExtras)
    grok.order(10)


class LocationThumbnailView(grok.View):
    grok.context(ILocation)
    grok.name('thumbnail_view')

    def update(self):
        self.url = self.context.absolute_url()
        self.title = self.context.Title()
        self.image = get_lead_image(self.context, size='mini')
