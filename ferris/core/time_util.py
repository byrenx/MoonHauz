import pytz
from . import settings


def utc_tz():
    return pytz.timezone('UTC')


def local_tz():
    return pytz.timezone(settings.get('timezone')['local'])


def localize(dt, tz=None):
    if not dt.tzinfo:
        dt = utc_tz().localize(dt)
    if not tz:
        tz = local_tz()
    return dt.astimezone(tz)
