from django.contrib import admin
from .models import Customer, Session


class CustomerBoard (admin.ModelAdmin) :
    list_display = ['name','car','is_checked']

class SessionBoard (admin.ModelAdmin) : 
    list_display = ['car', 'created_at','is_active']

admin.site.register(Customer, CustomerBoard)
admin.site.register(Session, SessionBoard)