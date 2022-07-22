import django
from django.core.mail import send_mail
from django.core.mail import EmailMessage
import random

from users.models import CustomUser

def send_confirmation_email(user):
    subject = 'Confirm your registration'
    OTP = random.randint(100000, 999999)
    message = f'Your Confirmation OTP is : {OTP}'
    from_email = django.conf.settings.EMAIL_HOST_USER
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list)
    user.otp = OTP
    user.save()
    return OTP




    