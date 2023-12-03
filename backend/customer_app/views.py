from django.shortcuts import render, HttpResponse, get_object_or_404
from .models import Session, Customer
from rest_framework.response import Response
from .models import Customer
from rest_framework import decorators, permissions, status, authentication
from car_app.models import Car

@decorators.api_view(['POST'])
@decorators.permission_classes([permissions.IsAuthenticated])
@decorators.authentication_classes([authentication.TokenAuthentication])
def check_customer_ticket(request, customeruuid ):
    
    try : 
        car = Car.objects.get(user=request.user)
        session = Session.objects.get(car=car,is_active=True)
        
        try : 
            customer = Customer.objects.get(uuid=customeruuid)
        except Customer.DoesNotExist :
            return Response({
                'message' : 'customer did not found'
            },status=status.HTTP_404_NOT_FOUND)
        

        if customer not in session.customers.all() or customer.is_checked == True: 
            return Response({    
                'message' : 'invalid customer'
            }, status=status.HTTP_400_BAD_REQUEST)


        customer.is_checked = True
        customer.save()

        return Response({'count':session.customers.filter(is_checked=True).count()},status=status.HTTP_200_OK)
        

    except Exception as error :
        return Response({
            'message' : f'an error accured : {error}'
        },status=status.HTTP_400_BAD_REQUEST)



@decorators.api_view(['POST'])
def create_customer (request, sessionuuid) : 
    
    session = get_object_or_404(Session,uuid=sessionuuid)

    try : 
        car = session.car

        if session.customers.count() >= car.maximum_users : 
            session.is_active = False
            session.save()
            return Response({'message':'car has maximum users'},status=status.HTTP_404_NOT_FOUND)

    
        if session.is_active == False : 
            return Response({'message':'session expired'},status=status.HTTP_400_BAD_REQUEST)

        
        customer_name = request.data.get('customer_name', None)

        if customer_name == None : 
            return RecursionError({'message':"customer_name field cannot be empty"},status=status.HTTP_400_BAD_REQUEST)
        
        customer = Customer.objects.create(name=customer_name,car=car)

        session.customers.add(customer)
        session.save()
        
        response = {
            'ticket' : f'media/tickets/{customer.uuid}.png' 
        }
        
        
        return Response(response,status=status.HTTP_200_OK)
    except Exception as error : 
        return Response({'message':f'error : {error}'},status=status.HTTP_400_BAD_REQUEST)
