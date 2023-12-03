from rest_framework import decorators, permissions, authentication, status
from rest_framework.response import Response



@decorators.api_view(['GET'])
@decorators.permission_classes([permissions.IsAuthenticated])
@decorators.authentication_classes([authentication.TokenAuthentication])
def UserDetails (request) : 
    user = request.user

    context = {
        'full_name' : user.full_name,
        'picture' : user.picture.url,
    }

    return Response(context,status=status.HTTP_200_OK)