from icalendar import Calendar, Event
from meetit.directions import journey
import urllib
import pytz
from dateutil.parser import *
from django.conf import settings


def parse_cal(url):
    data = urllib.urlopen(url).read()

    cal = Calendar.from_string(data)
    
    events = [ make_dict(ev) for ev in cal.subcomponents]
    
    return events

def to_local(dt):
    utc = pytz.utc
    local = pytz.timezone(settings.TIME_ZONE)
    if not str(dt.tzname()) == str(utc):
        dt = utc.localize(dt)
    return dt.astimezone(local)

def make_dict(ev):
    ev_dict = {
            "name": str(ev['SUMMARY']),
            "start": to_local(parse(str(ev['DTSTART']))),
            "end": to_local(parse(str(ev['DTEND']))),
            "location": str(ev['LOCATION'])
            }

    return ev_dict

def create_journey(origin, event):
    departure_time, arrival_time = journey(origin, event['location'], event['start'])
    ev_name = "%s Journey" % event['name']
    ev = Event()
    ev.add('dtstart', departure_time)
    ev.add('dtend', arrival_time)
    ev.add('summary', ev_name)

    return ev
