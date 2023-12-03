from django.urls import path
from .auth import login, register, get


urlpatterns = [
    path('login/',login.LoginView),
    path('register/',register.RegisterView),
    path('info/',get.UserDetails),
]