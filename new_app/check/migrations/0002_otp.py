# Generated by Django 4.1.13 on 2024-09-16 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('check', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OTP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('otp_code', models.CharField(max_length=6)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('expired_at', models.DateTimeField()),
            ],
        ),
    ]
