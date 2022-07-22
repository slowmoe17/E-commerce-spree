from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _


from .managers import CustomUserManager
class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=200 , null=True, blank=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    


