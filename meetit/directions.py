import urllib
import datetime
import simplejson
from dateutil.parser import *

def journey(origin, destination, start_time):
    url = 'http://maps.googleapis.com/maps/api/directions/json?origin=%s&destination=%s&sensor=false' % (urllib.quote(origin), urllib.quote(destination))
    
    data = urllib.urlopen(url)
    json_data = simplejson.load(data)

    print 'json'
    # print json_data
    
    if json_data['status'] != 'OK':
        print 'wtf'
        print json_data
        return False
    
    journey_length = datetime.timedelta(seconds = json_data['routes'][0]['legs'][0]['duration']['value'])
    
    # print journey_length, start_time
    ten_minutes = datetime.timedelta(minutes=10)

    print '#############'
    print 'ten: ',ten_minutes
    print 'start: ',start_time
    print 'start-10: ',parse(start_time) - ten_minutes
    arrival_time = parse(start_time) - ten_minutes
    print 'arrival: ',arrival_time
    print '#############'
    departure_time = arrival_time - journey_length

    print departure_time, arrival_time

    return departure_time, arrival_time
