from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from .models import Account, Category, Transaction, Todo, Task, ChecklistItem, Journal
from .serializers import AccountSerializer, CategorySerializer, TransactionSerializer, TodoSerializer, TaskSerializer, ChecklistItemSerializer, JournalSerializer, DashboardSerializer
from .filters import AccountFilter, CategoryFilter, TransactionFilter, TodoFilter, TaskFilter, ChecklistItemFilter, JournalFilter
from django.db.models import Sum
from datetime import datetime
today = datetime.today()

# Create your views here.

@api_view(['POST'])
@permission_classes([AllowAny])
def test_token(request):
    return Response({
        'message': 'Token is valid'
    }, status=status.HTTP_200_OK)

class Dashboard(APIView):
    serializer_class = DashboardSerializer

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        return Response({
            'status': 'success',
            'message': 'Dashboard retrieved successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

class AccountList(generics.ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AccountFilter
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
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


class AccountDeails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

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


class CategoryListCreate(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CategoryFilter
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        return Response({
            'status': 'success',
            'message': 'Categories retrieved successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'success',
                'message': 'Category created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            'status': 'error',
            'message': 'Failed to create category',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Category.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return Response({
            'status': 'success',
            'message': 'Category retrieved successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response({
                'status': 'success',
                'message': 'Category updated successfully',
                'data': serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            'status': 'error',
            'message': 'Failed to update category',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()

        return Response({
            'status': 'success',
            'message': 'Category deleted successfully'
        }, status=status.HTTP_200_OK)


class TransactionList(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TransactionFilter
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        transactions = self.filter_queryset(self.get_queryset())

        credited = transactions.filter(type='credit').aggregate(total_amount=Sum('amount'))['total_amount'] or 0.0
        debited = transactions.filter(type='debit').aggregate(total_amount=Sum('amount'))['total_amount'] or 0.0
        balance = float(credited) - float(debited)

        serializer = self.get_serializer(transactions, many=True)

        return Response({
            'status': 'success',
            'message': 'Transactions retrieved successfully',
            'data': serializer.data,
            'credited': credited,
            'debited': debited,
            'balance': balance
        }, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'success',
                'message': 'Transaction created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            'status': 'error',
            'message': 'Failed to create transaction',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class TransactionDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return Response({
            'status': 'success',
            'message': 'Transaction retrieved successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response({
                'status': 'success',
                'message': 'Transaction updated successfully',
                'data': serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            'status': 'error',
            'message': 'Failed to update transaction',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()

        return Response({
            'status': 'success',
            'message': 'Transaction deleted successfully'
        }, status=status.HTTP_200_OK)


class TaskList(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TaskFilter
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        return Response({
            'status': 'success',
            'message': 'Tasks retrieved successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'success',
                'message': 'Task created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            'status': 'error',
            'message': 'Failed to create task',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class TaskDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return Response({
            'status': 'success',
            'message': 'Task retrieved successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response({
                'status': 'success',
                'message': 'Task updated successfully',
                'data': serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            'status': 'error',
            'message': 'Failed to update task',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()

        return Response({
            'status': 'success',
            'message': 'Task deleted successfully'
        }, status=status.HTTP_200_OK)


class TodoList(generics.ListCreateAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TodoFilter
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        todos = self.filter_queryset(self.get_queryset())

        high = todos.filter(priority='high').count()
        normal = todos.filter(priority='normal').count()
        low = todos.filter(priority='low').count()

        serializer = self.get_serializer(todos, many=True)

        return Response({
            'status': 'success',
            'message': 'Todos retrieved successfully',
            'data': serializer.data,
            'high': high,
            'normal': normal,
            'low': low
        }, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'success',
                'message': 'Todo created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            'status': 'error',
            'message': 'Failed to create todo',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class TodoDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Todo.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return Response({
            'status': 'success',
            'message': 'Todo retrieved successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response({
                'status': 'success',
                'message': 'Todo updated successfully',
                'data': serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            'status': 'error',
            'message': 'Failed to update todo',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()

        return Response({
            'status': 'success',
            'message': 'Todo deleted successfully'
        }, status=status.HTTP_200_OK)

class CheckList(generics.ListCreateAPIView):
    queryset = ChecklistItem.objects.all()
    serializer_class = ChecklistItemSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ChecklistItemFilter
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(date=today)

        if not queryset.exists():
            tasks = Task.objects.all()
            checklist_objects = []

            for task in tasks:
                checklist_objects.append(ChecklistItem(task=task, date=today))

            ChecklistItem.objects.bulk_create(checklist_objects)

            queryset = self.filter_queryset(self.get_queryset())
            queryset = queryset.filter(date=today)

        serializer = self.get_serializer(queryset, many=True)

        return Response({
            'status': 'success',
            'message': 'Checklist retrieved successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'success',
                'message': 'Checklist created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            'status': 'error',
            'message': 'Failed to create checklist',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class CheckListDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ChecklistItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ChecklistItem.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return Response({
            'status': 'success',
            'message': 'Checklist retrieved successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response({
                'status': 'success',
                'message': 'Checklist updated successfully',
                'data': serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            'status': 'error',
            'message': 'Failed to update checklist',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()

        return Response({
            'status': 'success',
            'message': 'Checklist deleted successfully'
        }, status=status.HTTP_200_OK)

class PreviousDays(APIView):
    def get(self, request, *args, **kwargs):
        dates = sorted(set(ChecklistItem.objects.values_list('date', flat=True)), reverse=True)
        data = []

        for date in dates:
            tasks = ChecklistItem.objects.filter(date=date)
            completed = tasks.filter(completed=False).count() == 0

            data.append({'date': date, 'completed': completed})

        return Response({
            'status': 'success',
            'message': 'Dates retrieved successfully',
            'data': data
        }, status=status.HTTP_200_OK)

class PreviousDayTasks(generics.ListAPIView):
    queryset = ChecklistItem.objects.all()
    serializer_class = ChecklistItemSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ChecklistItemFilter
    ordering_fields = ['date']

class JournalList(generics.ListCreateAPIView):
    queryset = Journal.objects.all()
    serializer_class = JournalSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = JournalFilter
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        return Response({
            'status': 'success',
            'message': 'Journal retrieved successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'success',
                'message': 'Journal created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            'status': 'error',
            'message': 'Failed to create journal',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class JournalDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = JournalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Journal.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return Response({
            'status': 'success',
            'message': 'Journal retrieved successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response({
                'status': 'success',
                'message': 'Journal updated successfully',
                'data': serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            'status': 'error',
            'message': 'Failed to update journal',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()

        return Response({
            'status': 'success',
            'message': 'Journal deleted successfully'
        }, status=status.HTTP_200_OK)