from django import forms

class SignupForm(forms.Form):
    url = forms.URLField(verify_exists=True)
    postcode = forms.CharField(max_length=10)
