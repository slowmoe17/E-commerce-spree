from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import CustomUser
from users.mail import send_confirmation_email




@receiver(post_save, sender=CustomUser)
def send_verification_mail_to_user(sender, instance, created, **kwargs):
    if created:
        send_confirmation_email(instance)
        print("sent")
    








