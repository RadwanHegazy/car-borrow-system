from django.shortcuts import render
from rest_framework import decorators, status, authentication, permissions
from rest_framework.response import Response
from .models import Car
from customer_app.models import Session
from django.contrib.humanize.templatetags.humanize import naturaltime

@decorators.api_view(['GET'])
def get_avaliable_cars (request) :

    try : 

        sessions = Session.objects.filter(is_active=True)
        data = [session.car_details() for session in sessions]

        if 'from' or 'to' in request.GET :
            from_place = request.GET.get('from','')
            to_place = request.GET.get('to','') 

            if from_place or to_place : 
                cars = Car.objects.filter(from_place__icontains=from_place,to_place__icontains=to_place)
                data = []
                
                for car in cars :
                    sessions = Session.objects.filter(is_active=True,car=car)
                    data.append([session.car_details() for session in sessions])
            
        



        return Response(data,status=status.HTTP_200_OK)
    except Exception as error : 
        return Response({'message':f'error : {error}'},status=status.HTTP_400_BAD_REQUEST)
    

@decorators.api_view(['GET'])
@decorators.permission_classes([permissions.IsAuthenticated])
@decorators.authentication_classes([authentication.TokenAuthentication])
def car_owner_details(request) : 
    user = request.user
    
    car = Car.objects.get(user=user)
    sessions = Session.objects.filter(car=car).order_by('-created_at')
    data = []
    for session in sessions : 
        data.append({
            'date' : f'{naturaltime(session.created_at)}',
            'customers' : session.customers.filter(is_checked=True).count(),
            'total_price' : session.session_total_price(),
            'is_active' : session.is_active,
        })

    return Response(data,status=status.HTTP_200_OK)

@decorators.api_view(['POST'])
@decorators.permission_classes([permissions.IsAuthenticated])
@decorators.authentication_classes([authentication.TokenAuthentication])
def create_session (request) : 
    
    try : 
        user = request.user
        car = Car.objects.get(user=user)

        Session.objects.create(car=car).save()


        return Response({"message":'session opened successfully'},status=status.HTTP_200_OK)
    except Exception as error :
        return Response({"message":f'error : {error}'},status=status.HTTP_400_BAD_REQUEST)
        
    

@decorators.api_view(['POST'])
@decorators.permission_classes([permissions.IsAuthenticated])
@decorators.authentication_classes([authentication.TokenAuthentication])
def close_sessions (request) : 
    
    try : 
        user = request.user
        car = Car.objects.get(user=user)

        s = Session.objects.filter(car=car).order_by('-created_at')[0]
        s.is_active = False
        s.save()

        return Response({"message":'session closed successfully'},status=status.HTTP_200_OK)
    except Exception as error :
        return Response({"message":f'error : {error}'},status=status.HTTP_400_BAD_REQUEST)
        