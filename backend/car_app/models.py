from django.db import models
from user_app.models import User
from django.dispatch.dispatcher import receiver
from uuid import uuid4
from django.db.models.signals import post_save


class Car (models.Model) : 
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    maximum_users = models.IntegerField()
    from_place = models.CharField(max_length=100)
    to_place = models.CharField(max_length=100)
    price = models.FloatField()
    uuid = models.UUIDField(null=True,blank=True)
    car_number = models.CharField(max_length=20)

    def __str__(self) : 
        return f'{self.user.full_name} Car'
    



@receiver(post_save, sender = Car)
def CreateCarUUid (created, instance, **kwargs) : 
    if created : 
        instance.uuid = uuid4()
        instance.save()