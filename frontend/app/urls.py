from django.urls import path
from . import views, auth



urlpatterns = [
    path('',views.home,name='home'),
    
    path('driver/',views.driver,name='driver'),

    path('login/',auth.login,name='login'),
    path('register/',auth.register,name='register'),
    path('logout/',auth.logout,name='logout'),



]