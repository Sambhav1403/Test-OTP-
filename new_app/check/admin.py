from django.contrib import admin
from .models import Users, Blogs, Comments, OTP
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
# Register your models here

# accounts/admin.py

class OTPAdmin(admin.ModelAdmin):
    list_display = ('email', 'otp_code', 'created_at', 'expired_at', 'is_expired')
    actions = ['send_otp_email', 'verify_otp']

    def send_otp_email(self, request, queryset):
        for otp in queryset:
            if otp.is_expired():
                self.message_user(request, f'OTP for {otp.email} has expired.')
                continue
            
            send_mail(
                'Your OTP Code',
                f'Your OTP code is {otp.otp_code}. Please use this code to verify your email address.',
                'your-email@gmail.com',  # This should be the same as EMAIL_HOST_USER
                [otp.email],
                fail_silently=False,
            )
            self.message_user(request, f'OTP sent to {otp.email}.')
    
    send_otp_email.short_description = 'Send OTP via email'

    def verify_otp(self, request, queryset):
        for otp in queryset:
            if otp.is_expired():
                self.message_user(request, f'OTP for {otp.email} has expired.')
                continue
            
            otp.delete()  # Mark OTP as used
            self.message_user(request, f'OTP for {otp.email} verified.')
    
    verify_otp.short_description = 'Verify OTP'



admin.site.register(Users)
admin.site.register(Blogs)
admin.site.register(Comments)
admin.site.register(OTP, OTPAdmin)