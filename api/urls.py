from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from api import views

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('test/', views.test_token, name='test'),
    
    # Account endpoints
    path('accounts/', views.AccountListCreate.as_view(), name='accounts'),
    path('accounts/<int:pk>/', views.AccountRetrieveUpdateDelete.as_view(), name='account-detail'),
]