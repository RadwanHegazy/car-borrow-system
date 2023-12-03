from django.db import models
from car_app.models import Car
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from uuid import uuid4
import pyqrcode, os


class Customer (models.Model) : 
    name = models.CharField(max_length=200)
    is_checked = models.BooleanField(default=False)
    car = models.ForeignKey(Car,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    uuid = models.UUIDField(null=True,blank=True)


    def __str__ (self) : 
        return f'{self.name}'


class Session (models.Model) : 
    car = models.ForeignKey(Car,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    uuid = models.UUIDField(null=True,blank=True)
    customers = models.ManyToManyField(Customer,blank=True)

    def __str__(self) : 
        return f'{self.car.user.username} Car, {self.is_active}'


    def session_total_price (self) -> float: 
        return self.customers.filter(is_checked=True).count() * self.car.price

    def car_details (self) -> dict : 
        
        context = {
            'from' : self.car.from_place,
            'to' : self.car.to_place,
            'price' : self.car.price,
            'car_number' : self.car.car_number,
            'session_uuid' : self.uuid,
        }

        return context

@receiver(post_save,  sender=Session)
def Update_User_Session (created, instance, **kwargs) : 
    
    if created : 
        session = instance
        session.uuid = uuid4()
        session.save()

        userCar = session.car

        get_user_car = Session.objects.filter(car=userCar).order_by('-created_at')

        if get_user_car.count() > 1 :
            get_user_car = get_user_car[1]
            get_user_car.is_active = False
            
            get_user_car.save()


@receiver(post_save,sender=Customer)
def Update_Customer_uuid (created, instance, **kwargs) : 
    if created : 
        instance.uuid = uuid4()
        instance.save()

        # create customer ticket
        pyqrcode.create(str(instance.uuid)).png(f'media/tickets/{instance.uuid}.png',scale=6)
    

@receiver(post_delete,sender=Customer)
def DeleteCustomerTicket (instance, **kwargs) :
    try : 
        os.remove(f'media/tickets/{instance.uuid}.png')
    except Exception  : 
        pass