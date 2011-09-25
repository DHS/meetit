import urllib
import datetime
import simplejson

def journey(origin, destination, start_time):
    url = 'http://maps.googleapis.com/maps/api/directions/json?origin=%s&destination=%s&sensor=false' % (urllib.quote(origin), urllib.quote(destination))
    
    data = urllib.urlopen(url)
    json_data = simplejson.load(data)
    
    if json_data['status'] != 'OK':
        print json_data['status']
        return False
    
    journey_length = datetime.timedelta(seconds = json_data['routes'][0]['legs'][0]['duration']['value'])
    
    arrival_time = start_time - datetime.timedelta(minutes=10)
    departure_time = arrival_time - journey_length

    return departure_time, arrival_time
