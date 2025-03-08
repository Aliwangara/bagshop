from allauth.account.forms import SignupForm
from django import forms

class CustomSignupForm(SignupForm):
    email = forms.EmailField(required=True) 
