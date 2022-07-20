from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Cart, CartItem
from users.models import CustomUser
from django.contrib.auth.models import User


"""@receiver(pre_save,sender = get_user_model())
def create_cart(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user=instance)"""

# create cart for each user when user is created
@receiver(pre_save, sender=get_user_model)
def create_cart(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user=instance)


    

     










    





