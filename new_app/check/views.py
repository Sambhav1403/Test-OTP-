# otp/views.py
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.utils import timezone
from django.conf import settings
from django.http import HttpResponse
from .models import OTP
from .forms import OTPVerificationForm

def send_otp(email):
    otp = OTP(email=email)
    otp.save()
    send_mail(
        'Your OTP Code',
        f'Your OTP code is {otp.otp_code}. It expires in 5 minutes.',
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )

def generate_otp_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        send_otp(email)
        return HttpResponse('OTP sent to your email')
    return render(request, 'generate_otp.html')

def verify_otp_view(request):
    if request.method == 'POST':
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            otp = form.cleaned_data['otp']
            try:
                otp_record = OTP.objects.get(email=email, otp=otp)
                if otp_record.is_expired():
                    return HttpResponse('OTP has expired')
                return HttpResponse('OTP verified successfully')
            except OTP.DoesNotExist:
                return HttpResponse('Invalid OTP')
    else:
        form = OTPVerificationForm()
    return render(request, 'verify_otp.html', {'form': form})
