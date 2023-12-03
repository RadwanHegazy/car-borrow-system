from django.contrib import admin
from .models import User

class UserBoard ( admin.ModelAdmin ) :
    list_display = ['full_name','phone']

admin.site.register(User, UserBoard)