
import datetime
import pytz

from five import grok

from Products.ATContentTypes.interfaces.event import IATEvent
from Products.ATContentTypes.interfaces.folder import IATFolder
from Products.CMFCore.utils import getToolByName

from deaf.contents.browser.document import DocumentView, DocumentActions
from deaf.contents.browser.utils import get_category, convert_to_datetime
from deaf.contents.browser.utils import format_date, format_time
from deaf.contents.browser.utils import get_lead_image


def is_passed(date):
    """Return true if the given date is passed.
    """
    date = convert_to_datetime(date)
    if date is not None:
        now =  datetime.datetime.now(tz=pytz.timezone('Europe/Amsterdam'))
        return now > date
    return False


class EventFolderView(grok.View):
    grok.context(IATFolder)
    grok.name('event_folder_view')

    def update(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        metadata = getToolByName(self.context, 'portal_metadata').DCMI
        index = self.context._getOb('index', None)
        if index is not None:
            self.index = index.getText()
        else:
            self.index = None
        self.url = self.context.absolute_url()
        self.categories = ['All'] + list(metadata.getElementSpec(
                'Subject').getPolicy('Event').allowedVocabulary())

        query= dict(portal_type=('Event',),
                    path="/".join(self.context.getPhysicalPath()))
        subject = self.request.form.get('Subject')
        if subject not in (None, 'All',):
            query['Subject'] = subject

        # Sort event on position in the parent folder.
        query['sort_on'] = 'getObjPositionInParent'

        brains = list(catalog(**query))

        # Sort event on title
        # brains.sort(
        #     key=lambda b: b.Title and b.Title.lower() or None)

        # Sort on the subject
        # brains.sort(
        #     key=lambda b: b.Subject and b.Subject[0].lower() or None)

        self.events = map(lambda b: b.getObject(), brains)


class EventFolder2View(EventFolderView):
    grok.name('event_folder2_view')


class EventView(DocumentView):
    grok.context(IATEvent)
    grok.name('event_view')


def read_event(self, event):
    self.location = event.getLocation()
    self.dates = []
    for start, end in (
        ('startDate', 'endDate'),
        ('startDateExtraDay1', 'endDateExtraDay1'),
        ('startDateExtraDay2', 'endDateExtraDay2'),
        ('startDateExtraDay3', 'endDateExtraDay3'),
        ('startDateExtraDay4', 'endDateExtraDay4'),
        ('startDateExtraDay5', 'endDateExtraDay5')):
        date = format_date(event[start])
        start_time = format_time(event[start])
        end_time = format_time(event[end])
        if date is not None and end_time is not None:
            self.dates.append(
                {'day': date,
                 'start': start_time,
                 'end': end_time,
                 'raw_start': event[start],
                 'raw_end': event[end]})

    self.passed = False
    if self.dates:
        self.passed = is_passed(self.dates[-1]['raw_end'])
    self.category = get_category(event)


class EventDetails(grok.Viewlet):
    grok.context(IATEvent)
    grok.viewletmanager(DocumentActions)
    grok.order(20)

    def update(self):
        read_event(self, self.context)


class EventThumbnailView(grok.View):
    grok.context(IATEvent)
    grok.name('thumbnail_view')

    def update(self):
        self.title = self.context.Title()
        self.description = self.context.Description()
        self.url = self.context.absolute_url()
        read_event(self, self.context)


# This is used by EventFolder2View, an alternative display mode.
class EventThumbnail2View(grok.View):
    grok.context(IATEvent)
    grok.name('thumbnail2_view')

    def update(self):
        self.title = self.context.Title()
        self.url = self.context.absolute_url()
        self.photo = get_lead_image(self.context, size='mini')
