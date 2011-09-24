from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from meetit.forms import SignupForm
from meetit.calendar import parse_cal
from meetit.directions import journey
from django.views.decorators.csrf import csrf_exempt
from icalendar import Calendar, Event
import os
import time
import datetime
from django.conf import settings

@csrf_exempt
def signup(request):
    data = False

    if request.POST and 'signup' in request.POST:
        signupForm = SignupForm(request.POST)
        if signupForm.is_valid():
            #do shit
            signupCD = signupForm.cleaned_data
            data = parse_cal(signupCD['url'])
            origin = signupCD['postcode']
        else:
            #show errors
            pass
    else:
        signupForm = SignupForm()

    if data:
        return events(request, origin, data)
    else:
        return render_to_response('base_signup.html', locals())

@csrf_exempt
def events(request, origin, events):

    return render_to_response('base_events.html', locals())

@csrf_exempt
def journeys(request):
    new_events = []
    if request.POST and 'plan' in request.POST:
        origin = str(request.POST['origin'])
        events = eval(str(request.POST['events']))
        cal = Calendar()
        for i, event in enumerate(events):
            if request.POST.get('cb_%s' % str(i+1)):
                departure_time, arrival_time = journey(origin, event['location'], event['start'])
                ev_name = "%s Journey" % event['name']
                ev = Event()
                ev.add('dtstart', departure_time)
                ev.add('dtend', arrival_time)
                ev.add('summary', ev_name)
                cal.add_component(ev)

                new_events.append({'departure': departure_time, 'arrival': arrival_time, 'name': ev_name})

        # if not empty
        if cal.subcomponents:

            calfilename = 'calfile/meetit-%s.ics' % int(time.time())
            calfile = os.path.join(settings.MEDIA_ROOT, calfilename)

            f = open(calfile, 'wb')
            f.write(cal.as_string())
            f.close()

        else:
            cal_display = "no events!"

        return render_to_response('base_journeys.html', locals())

    else:
        return HttpResponseRedirect('/')

