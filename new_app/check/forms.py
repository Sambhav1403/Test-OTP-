# otp/forms.py
from django import forms

class OTPVerificationForm(forms.Form):
    email = forms.EmailField()
    otp = forms.CharField(max_length=6)
