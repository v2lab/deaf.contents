# This is a package

from five import grok


class Scripts(grok.DirectoryResource):
    grok.name('deaf.contents')
    grok.path('static')
