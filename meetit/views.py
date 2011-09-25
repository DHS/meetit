from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from meetit.forms import SignupForm
from meetit.calendar import *
from meetit.directions import journey
from meetit.gateways.email import generate_soap
from django.views.decorators.csrf import csrf_exempt
from icalendar import Calendar, Event
from dateutil.parser import *
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
			url = signupCD['url']
			if url[0:9] == 'webcal://':
				url = 'http' + url[6:]
			data = parse_cal(url)
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
    request.session['origin'] = origin
    request.session['events'] = events
    return render_to_response('base_events.html', locals())

@csrf_exempt
def journeys(request):
    new_events = []
    if request.POST and 'plan' in request.POST:
        origin = request.session.pop('origin')
        events = request.session.pop('events')
        cal = Calendar()
        for i, event in enumerate(events):
            if request.POST.get('cb_%s' % str(i+1)):
                ev = create_journey(origin, event)
                if ev: 
                    cal.add_component(ev)
                    new_events.append({'departure': to_local(parse(str(ev['dtstart']))), 'arrival': to_local(parse(str(ev['dtend']))), 'name': ev['summary']})

        # if not empty
        if cal.subcomponents:

            if request.POST.get('email'):
                address = request.POST.get('email_address')
                evs = len(new_events)
                title = "%s events" % evs if evs >= 2 else new_events[0]['name']
                generate_soap(address, cal, title)

                return HttpResponse('Email sent!')

            else:
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
