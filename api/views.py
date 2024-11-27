from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import generics
from .models import Account
from .serializers import AccountSerializer

# Create your views here.

@api_view(['POST'])
@permission_classes([AllowAny])
def test_token(request):
    return Response({
        'message': 'Token is valid'
    }, status=status.HTTP_200_OK)

class AccountListCreate(generics.ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        return Response({
            'status': 'success',
            'message': 'Accounts retrieved successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'success',
                'message': 'Account created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            'status': 'error',
            'message': 'Failed to create account',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class AccountRetrieveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AccountSerializer
    
    def get_queryset(self):
        return Account.objects.all()
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return Response({
            'status': 'success',
            'message': 'Account retrieved successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        
        if serializer.is_valid():
            serializer.save()

            return Response({
                'status': 'success',
                'message': 'Account updated successfully',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
            
        return Response({
            'status': 'error',
            'message': 'Failed to update account',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()

        return Response({
            'status': 'success',
            'message': 'Account deleted successfully'
        }, status=status.HTTP_200_OK)