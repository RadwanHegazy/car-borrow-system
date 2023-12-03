from django.contrib import admin
from .models import Car


class CarBoard (admin.ModelAdmin) : 
    list_display = ['user','from_place','to_place','price','car_number']

admin.site.register(Car, CarBoard)