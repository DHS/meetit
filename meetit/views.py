from django.http import HttpResponse
from django.shortcuts import render_to_response
from meetit.forms import SignupForm

def signup(request):
    data = False

    if request.POST and 'signup' in request.POST:
        signupForm = SignupForm(request.POST)
        if signupForm.is_valid():
            #do shit
            data = True

        else:
            #show errors
            pass
    else:
        signupForm = SignupForm()

    if data:
        return render_to_response('base_events.html', locals())
    else:
        return render_to_response('base_signup.html', locals())

