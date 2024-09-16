from django.db import models
from django.utils import timezone
import random
import string


class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(unique=True, max_length=50, blank=True)  # Avoid `null=True` if it causes issues
    email = models.EmailField(unique=True, blank=True)  # Using `EmailField` for better validation
    password = models.TextField(blank=True)  # Avoid `null=True`
    created_at = models.DateTimeField(auto_now_add=True, blank=True)  # Use `auto_now_add=True` to handle creation time


class Blogs(models.Model):
    blog_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, blank=True)  # Use `SET_NULL` and avoid `null=False`
    title = models.CharField(max_length=255, blank=True)  # Avoid `null=True`
    content = models.TextField(blank=True)  # Avoid `null=True`
    created_at = models.DateTimeField(auto_now_add=True, blank=True)  # Use `auto_now_add=True`


class Comments(models.Model):
    comment_id = models.AutoField(primary_key=True)
    blog = models.ForeignKey(Blogs, on_delete=models.SET_NULL, null=True, blank=True)  # Use `SET_NULL`
    user = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, blank=True)  # Use `SET_NULL`
    comment_text = models.TextField(blank=True)  # Avoid `null=True`
    created_at = models.DateTimeField(auto_now_add=True, blank=True)  # Use `auto_now_add=True`

# accounts/models.py

class OTP(models.Model):
    email = models.EmailField()
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField()

    def is_expired(self):
        return timezone.now() > self.expired_at

    @staticmethod
    def generate_otp():
        return ''.join(random.choices(string.digits, k=6))

    def save(self, *args, **kwargs):
        # Set the `expired_at` field before saving
        if not self.expired_at:
            self.otp_code = self.generate_otp()
            self.expired_at = timezone.now() + timezone.timedelta(hours=1)  # Example: OTP expires in 1 hour
        super().save(*args, **kwargs)