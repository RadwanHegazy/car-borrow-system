from rest_framework.response import Response
from rest_framework import decorators, status
from rest_framework.authtoken.models import Token
from ..models import User

@decorators.api_view(['POST'])
def LoginView (request): 

    phone = request.data.get('phone',None)
    password = request.data.get('password',None)

    if phone == None : 
        return Response({'message':'phone field can not be empty'},status=status.HTTP_400_BAD_REQUEST)
    
    if password == None : 
        return Response({'message':'password field can not be empty'},status=status.HTTP_400_BAD_REQUEST)
    
    auth = User.login(phone=phone,password=password)

    if auth['errors'] : 
        return Response(auth,status=status.HTTP_400_BAD_REQUEST)

    user_token = auth['user_token']

    return Response({'token':user_token},status=status.HTTP_200_OK)