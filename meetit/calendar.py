from icalendar import Calendar
from datetime import datetime
import urllib


def parse_cal(url):
    data = urllib.urlopen(url).read()

    cal = Calendar.from_string(data)
    
    events = [ make_dict(ev) for ev in cal.subcomponents]
    
    return events

def make_dict(ev):
    ev_dict = {
            "name": str(ev['SUMMARY']),
            "start": datetime.strptime(str(ev['DTSTART']), "%Y%m%dT%H%M00Z"),
            "end": datetime.strptime(str(ev['DTEND']), "%Y%m%dT%H%M00Z"),
            "location": str(ev['LOCATION'])
            }

    return ev_dict
