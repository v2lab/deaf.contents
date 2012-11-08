
from Acquisition import aq_parent
from Products.ATContentTypes.interfaces.document import IATDocument
from Products.ATContentTypes.interfaces.interfaces import IATContentType
from Products.CMFCore.utils import getToolByName

from deaf.contents.buyable_content import IBuyableContent
from deaf.contents.browser.utils import get_lead_image
from collective.contentleadimage.interfaces import ILeadImageable
from five import grok
from plone.theme.interfaces import IDefaultPloneLayer
from plone.app.layout.nextprevious.interfaces import INextPreviousProvider
from zope.i18nmessageid import MessageFactory

_ = MessageFactory('deaf.contents')

grok.layer(IDefaultPloneLayer)


class DocumentView(grok.View):
    grok.context(IATDocument)
    grok.name('document_view')

    RELATED_LABELS = {
        'Event': _(u'Events'),
        'News Item': _(u'News Items'),
        'Link': _(u'V2 Archives'),
        'Document': _(u'Program Items'),
        'Person': _(u'Artists/Speakers'),
        'GeoLocation': _(u'Locations')}

    def update(self):
        self.title = self.context.Title()
        self.description = self.context.Description()
        self.url = self.context.absolute_url()
        self.css_class = self.context.portal_type.replace(' ', '-').lower()

        # Validate related are published
        member = getToolByName(self, 'portal_membership')
        if member.isAnonymousUser():
            workflow = getToolByName(self, 'portal_workflow')

            def validate(content):
                if content is None:
                    return False
                if content.portal_type in ('File', 'Image'):
                    return True
                return workflow.getInfoFor(
                    content, 'review_state') == 'published'
        else:
            validate = lambda content: content is not None

        # Collect related
        related_by_type = {}
        for related in self.context.getRefs():
            if validate(related):
                related_by_type.setdefault(related.portal_type, [])
                related_by_type[related.portal_type].append(related)

        # Build a nice data structure for the template
        self.related = []
        for key, label in self.RELATED_LABELS.iteritems():
            if key in related_by_type:
                self.related.append(
                    {'title': label,
                     'contents': related_by_type[key]})


class DocumentActions(grok.ViewletManager):
    grok.context(IATContentType)
    grok.view(DocumentView)
    grok.name('deaf.actions')

    def update(self):
        self.next = None
        self.previous = None
        provider = INextPreviousProvider(aq_parent(self.context), None)
        if provider is not None:
            self.next = provider.getNextItem(self.context)
            self.previous = provider.getPreviousItem(self.context)
        super(DocumentActions, self).update()


class DocumentExtras(grok.ViewletManager):
    grok.context(IATContentType)
    grok.view(DocumentView)
    grok.name('deaf.document.extra')


class DocumentLeadImageExtra(grok.Viewlet):
    grok.context(ILeadImageable)
    grok.viewletmanager(DocumentExtras)
    grok.order(10)

    def available(self):
        return self.image['url'] is not None

    def update(self):
        self.image = get_lead_image(self.context, size='preview')


class ShareLink(grok.Viewlet):
    grok.context(IATContentType)
    grok.viewletmanager(DocumentActions)
    grok.order(50)


class BuyTicketLink(grok.Viewlet):
    grok.context(IATContentType)
    grok.viewletmanager(DocumentActions)
    grok.order(60)

    def available(self):
        return bool(self.url)

    def update(self):
        self.url = None
        provider = IBuyableContent(self.context, None)
        if provider is not None:
            self.url = provider.webshop_url
