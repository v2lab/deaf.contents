
from five import grok
from z3c.form import form, field
from zope import schema
from zope.annotation import IAnnotations
from zope.interface import Interface
from Products.ATContentTypes.interfaces.interfaces import IATContentType


class IBuyableContent(Interface):

    webshop_url = schema.TextLine(
        title=u"Webshop URL",
        description=u"URL to which the visitor should be redirected " + \
            "to be able to buy the content.",
        required=False)


BASE_KEY = 'deaf.buyable_content.'


def make_property(key, default):
    key = BASE_KEY + key

    def setter(self, value):
        self._data[key] = value
    def getter(self):
        return self._data.get(key, default)
    return property(getter, setter)


class BuyableAdapter(grok.Adapter):
    grok.context(IATContentType)
    grok.implements(IBuyableContent)

    def __init__(self, context):
        self.context = context
        self._data = IAnnotations(context)

    @apply
    def webshop_url():
        return make_property('webshop_url', u'')


class EditBuyableInformation(form.EditForm):
    fields = field.Fields(IBuyableContent)
