from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from api import views

urlpatterns = [
    # Account endpoints
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('test/', views.test_token, name='test'),

    # Dashboard endpoints
    # path('dashboard/', views.Dashboard.as_view(), name='dashboard'),
    
    # Account endpoints
    path('accounts/', views.AccountList.as_view(), name='accounts'),
    path('accounts/<int:pk>/', views.AccountDeails.as_view(), name='account-detail'),

    # category endpoints
    path('categories/', views.CategoryListCreate.as_view(), name='categories'),
    path('categories/<int:pk>/', views.CategoryDetails.as_view(), name='category-detail'),

    # transaction endpoints
    path('transactions/', views.TransactionList.as_view(), name='transactions'),
    path('transactions/<int:pk>/', views.TransactionDetails.as_view(), name='transaction-detail'),

    # task endpoints
    path('tasks/', views.TaskList.as_view(), name='tasks'),
    path('tasks/<int:pk>/', views.TaskDetails.as_view(), name='task-detail'),

    # todo endpoints
    path('todos/', views.TodoList.as_view(), name='todos'),
    path('todos/<int:pk>/', views.TodoDetails.as_view(), name='todo-detail'),

    # checklist endpoints
    path('checklists/', views.CheckList.as_view(), name='checklists'),
    path('checklists/<str:date>/', views.CheckListDetails.as_view(), name='checklist-detail'),

    # journal endpoints
    path('journals/', views.JournalList.as_view(), name='journals'),
    path('journals/<str:date>/', views.JournalDetails.as_view(), name='journal-detail'),
]