from . import views
from django.urls import path

urlpatterns = [
    path('create/<str:sessionuuid>/',views.create_customer),
    path('check/ticket/<str:customeruuid>',views.check_customer_ticket)
]