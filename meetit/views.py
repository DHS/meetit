from django.shortcuts import render_to_response
from meetit.forms import SignupForm
from meetit.calendar import parse_cal
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def signup(request):
    data = False

    if request.POST and 'signup' in request.POST:
        signupForm = SignupForm(request.POST)
        if signupForm.is_valid():
            #do shit
            signupCD = signupForm.cleaned_data
            data = parse_cal(signupCD['url'])
        else:
            #show errors
            pass
    else:
        signupForm = SignupForm()

    if data:
        return events(request, data)
    else:
        return render_to_response('base_signup.html', locals())

def events(request, data):

    return render_to_response('base_events.html', locals())


