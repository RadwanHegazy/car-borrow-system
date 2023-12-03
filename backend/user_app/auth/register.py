from rest_framework.response import Response
from rest_framework import decorators, status
from rest_framework.authtoken.models import Token
from ..models import User
from car_app.models import Car
from rest_framework.authtoken.models import Token



@decorators.api_view(['POST'])
def RegisterView (request) : 

    try : 
        # user details
        image = request.data.get('image', None)
        full_name = request.data.get('full_name', None)
        phone = request.data.get('phone', None)
        password = request.data.get('password', None)

        if image is None or full_name is None  or phone is None or password is None : 
            return Response({'messsage':"there is field is empty"},status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(
            phone = phone,
            full_name = full_name,
            password = password,
            picture = image
        )

        response = {
            'token' : Token.objects.get(user=user).key
        }

        # car details
        car_number = request.data.get('car_number', None)
        from_place = request.data.get('from',None)
        to_place = request.data.get('to',None)
        price = request.data.get('price',None)
        maximum_users = request.data.get('maximum_users',None)
        
        if car_number is None or maximum_users is None or from_place is None  or to_place is None or price is None : 
            return Response({'messsage':"field is empty"},status=status.HTTP_400_BAD_REQUEST)

        Car.objects.create(
            user = user,
            maximum_users = maximum_users,
            from_place = from_place,
            to_place = to_place,
            price = price,
            car_number = car_number
        ).save()


        return Response(response,status=status.HTTP_200_OK)
    except Exception as error :
        return Response({'message':f'error : {error}'},status=status.HTTP_400_BAD_REQUEST)
    