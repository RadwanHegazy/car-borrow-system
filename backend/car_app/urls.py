from .views import get_avaliable_cars, close_sessions, car_owner_details, create_session
from django.urls import path


urlpatterns = [
    path('',get_avaliable_cars),
    path('session/get/',car_owner_details),
    path('session/create/',create_session),
    path('session/close/',close_sessions),
]