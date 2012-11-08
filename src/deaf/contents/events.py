
from zope.component import adapts
from zope.interface import implements
from archetypes.schemaextender.interfaces import ISchemaExtender
from archetypes.schemaextender.field import ExtensionField

from Products.ATContentTypes.interfaces import IATEvent
from Products.Archetypes.atapi import CalendarWidget
from Products.Archetypes.atapi import DateTimeField
from Products.CMFCore.permissions import ModifyPortalContent


class ExtraDateTimeField(ExtensionField, DateTimeField):
    pass


class EventExtender(object):
    adapts(IATEvent)
    implements(ISchemaExtender)

    fields = [
            ExtraDateTimeField('startDateExtraDay1',
                  required=False,
                  searchable=False,
                  write_permission = ModifyPortalContent,
                  languageIndependent=True,
                  widget = CalendarWidget(
                        description= '',
                        label=u'Event start extra day 1',
                        )),
            ExtraDateTimeField('endDateExtraDay1',
                  required=False,
                  searchable=False,
                  write_permission = ModifyPortalContent,
                  languageIndependent=True,
                  widget = CalendarWidget(
                        description = '',
                        label = u'Event end extra day 1'
                        )),
            ExtraDateTimeField('startDateExtraDay2',
                  required=False,
                  searchable=False,
                  write_permission = ModifyPortalContent,
                  languageIndependent=True,
                  widget = CalendarWidget(
                        description= '',
                        label=u'Event start extra day 2',
                        )),
            ExtraDateTimeField('endDateExtraDay2',
                  required=False,
                  searchable=False,
                  write_permission = ModifyPortalContent,
                  languageIndependent=True,
                  widget = CalendarWidget(
                        description = '',
                        label = u'Event end extra day 2'
                        )),
            ExtraDateTimeField('startDateExtraDay3',
                  required=False,
                  searchable=False,
                  write_permission = ModifyPortalContent,
                  languageIndependent=True,
                  widget = CalendarWidget(
                        description= '',
                        label=u'Event start extra day 3',
                        )),
            ExtraDateTimeField('endDateExtraDay3',
                  required=False,
                  searchable=False,
                  write_permission = ModifyPortalContent,
                  languageIndependent=True,
                  widget = CalendarWidget(
                        description = '',
                        label = u'Event end extra day 3'
                        )),
            ExtraDateTimeField('startDateExtraDay4',
                  required=False,
                  searchable=False,
                  write_permission = ModifyPortalContent,
                  languageIndependent=True,
                  widget = CalendarWidget(
                        description= '',
                        label=u'Event start extra day 4',
                        )),
            ExtraDateTimeField('endDateExtraDay4',
                  required=False,
                  searchable=False,
                  write_permission = ModifyPortalContent,
                  languageIndependent=True,
                  widget = CalendarWidget(
                        description = '',
                        label = u'Event end extra day 4'
                        )),
            ExtraDateTimeField('startDateExtraDay5',
                  required=False,
                  searchable=False,
                  write_permission = ModifyPortalContent,
                  languageIndependent=True,
                  widget = CalendarWidget(
                        description= '',
                        label=u'Event start extra day 5',
                        )),
            ExtraDateTimeField('endDateExtraDay5',
                  required=False,
                  searchable=False,
                  write_permission = ModifyPortalContent,
                  languageIndependent=True,
                  widget = CalendarWidget(
                        description = '',
                        label = u'Event end extra day 5'
                        )),
        ]

    def __init__(self, context):
         self.context = context

    def getFields(self):
        return self.fields
