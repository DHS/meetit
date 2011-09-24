from django import forms

class SignupForm(forms.Form):
    url = forms.CharField(max_length=200)
    postcode = forms.CharField(max_length=10)
