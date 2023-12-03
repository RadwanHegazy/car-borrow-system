from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from uuid import uuid4
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework.authtoken.models import Token


class User (AbstractUser):
    username = None
    groups = None
    first_name = None
    last_name = None


    picture = models.ImageField(upload_to='users-images/',default='default.png')
    full_name = models.CharField(_('Full Name'),max_length=100)
    phone = PhoneNumberField(_("phone number"),unique=True,default='+2')
    uuid = models.UUIDField(null=True,blank=True)

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ['full_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.full_name
    
    def login (**kwargs) : 
        phone = kwargs['phone']
        password = kwargs['password']

        user = User.objects.filter(phone=phone)
        
        response = {
            'errors':''
        }

        if not user.exists() or user.count() > 1 :
            response['errors'] = 'invalid phone number'
            return response
        
        user = user.first()

        if not user.check_password(password) :
            response['errors'] = 'invalid password'
            return response
        
        response['user_token'] = Token.objects.get(user=user).key

        return response

@receiver(post_save, sender = User)
def GenreateHashKey (created, instance, **kwargs) :
    if created :
        instance.uuid = uuid4()
        Token.objects.create(user=instance).save()
        instance.save()