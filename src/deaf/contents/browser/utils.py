
from DateTime import DateTime
from datetime import datetime

from collective.contentleadimage.config import IMAGE_FIELD_NAME
from collective.contentleadimage.config import IMAGE_CAPTION_FIELD_NAME
from collective.contentleadimage.interfaces import ILeadImageable


def get_lead_image(content, size='preview'):
    url = None
    caption = None
    if ILeadImageable.providedBy(content):
        field = content.getField(IMAGE_FIELD_NAME)
        if field is not None and field.get(content):
            url = ''.join((content.absolute_url(), '/leadImage_', size))
            field_caption = content.getField(
                IMAGE_CAPTION_FIELD_NAME)
            if field_caption is not None:
                caption = field_caption.get(content)
    return {'url': url, 'caption': caption}


def get_category(content):
    subjects = content.Subject()
    if subjects:
        return subjects[0]
    return None

def convert_to_datetime(date):
    if date in (None, 'None'):
        return None
    if isinstance(date, basestring):
        date = DateTime(date)
    if isinstance(date, DateTime):
        date = date.asdatetime()
    return date

def format_date(date):
    if date in (None, 'None'):
        return None
    if isinstance(date, basestring):
        date = DateTime(date)
    elif isinstance(date, datetime):
        date = date.date()
    return date.strftime('%d.%m.%Y')

def format_time(time):
    if time in (None, 'None'):
        return None
    elif isinstance(time, datetime):
        time = time.time()
    return time.strftime('%H:%M')
