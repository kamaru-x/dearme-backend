from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

# Create your views here.

@api_view(['POST'])
@permission_classes([AllowAny])
def test_token(request):
    return Response({
        'message': 'Token is valid'
    }, status=status.HTTP_200_OK)
