from django.shortcuts import render_to_response
from meetit.forms import SignupForm
from meetit.calendar import parse_cal
from meetit.directions import journey
from django.views.decorators.csrf import csrf_exempt
from icalendar import Calendar, Event

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

def events(request, origin, events):
	cal = Calendar()
	for event in events:
		try:
			departure_time, arrival_time = journey(origin, event['location'], event['start'])
		except TypeError:
			pass
		else:
			ev = Event()
			ev.add('dtstart', departure_time)
			ev.add('dtend', arrival_time)
			ev.add('summary', "%s Journey" % event['name'])
			cal.add_component(ev)
	cal_display = cal.as_string()
	return render_to_response('base_events.html', locals())


