from icalendar import Calendar, Event
from meetit.directions import journey
import urllib
import pytz
import datetime
from dateutil.parser import *
from django.conf import settings


def parse_cal(url):
    data = urllib.urlopen(url).read()
    cal = Calendar.from_string(data)
    
    an_hour_ago = to_local(datetime.datetime.now() - datetime.timedelta(hours=1))

    events = []
    for ev in cal.walk():
        if ev.name == 'VEVENT':
            start = to_local(parse(str(ev['dtstart'])))
            if start.time() and start >= an_hour_ago and ev['LOCATION']:
                events.append(make_dict(ev))
    
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
    try:
        departure_time, arrival_time = journey(origin, event['location'], event['start'])
    except TypeError, e:
        print 'wtf2 ', e
        return False
    else:
        ev_name = "%s Journey" % event['name']
        ev = Event()
        ev.add('dtstart', departure_time)
        ev.add('dtend', arrival_time)
        ev.add('summary', ev_name)

        return ev
