from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from .models import Account, Category, Transaction, SelfTransfer, Todo, Task, ChecklistItem, Journal
from .serializers import AccountSerializer, CategorySerializer, TransactionSerializer, SelfTransferSerializer, TodoSerializer, TaskSerializer, ChecklistItemSerializer, JournalSerializer, DashboardSerializer
from .filters import AccountFilter, CategoryFilter, TransactionFilter, TodoFilter, TaskFilter, ChecklistItemFilter, JournalFilter
from django.db.models import Sum, Count
from datetime import datetime, date
from collections import defaultdict
from decimal import Decimal
today = datetime.today()

# Create your views here.

################################################## TEST TOKEN ##################################################

@api_view(['POST'])
@permission_classes([AllowAny])
def test_token(request):
    return Response({
        'message': 'Token is valid'
    }, status=status.HTTP_200_OK)

################################################## DASHBOARD ##################################################

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

################################################## ACCOUNTS LIST & CREATE ##################################################

class AccountList(generics.ListCreateAPIView):
    serializer_class = AccountSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AccountFilter
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)

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
            serializer.save(user=request.user)
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

################################################## ACCOUNTS UPDATE & DELETE ##################################################

class AccountDeails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)

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

################################################## CATEGORIES LIST & CREATE ##################################################

class CategoryListCreate(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CategoryFilter
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

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
            serializer.save(user=request.user)
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


################################################## CATEGORY UPDATE & DELETE ##################################################

class CategoryDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

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

################################################## TRANSACTION OVERVIEW ##################################################

class TransactionOverview(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        categories = Category.objects.filter(user=request.user)
        totals = []

        for category in categories:
            transactions = Transaction.objects.filter(category=category, user=request.user)
            amount = (transactions.aggregate(total_amount=Sum('amount'))['total_amount'] or 0.0)

            total = {
                'category': category.name,
                'type' : category.type.capitalize(),
                'transactions': f'{transactions.count()} transactions',
                'amount': amount,
            }

            totals.append(total)

        return Response({
            'status': 'success',
            'message': 'Transaction overview retrieved successfully',
            'data': totals,
        }, status=status.HTTP_200_OK)

################################################## TRANSACTION REPORT ##################################################

class TransactionReport(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Fetch all transactions
        transactions = Transaction.objects.filter(user=request.user).exclude(account__type='savings_account')

        # Initialize a dictionary to hold credit, debit, and balance for each (year, month)
        monthly_data = defaultdict(lambda: {'credit': float('0.0'), 'debit': float('0.0'), 'balance': float('0.0')})

        for transaction in transactions:
            year = transaction.date.year
            month = transaction.date.month
            key = (year, month)

            # Ensure that amounts are converted to Decimal for consistent type handling
            amount = float(transaction.amount)

            if transaction.category.type == 'credit':
                monthly_data[key]['credit'] += amount
            elif transaction.category.type == 'debit':
                monthly_data[key]['debit'] += amount

            # Calculate balance as credit - debit
            monthly_data[key]['balance'] = monthly_data[key]['credit'] - monthly_data[key]['debit']

        # Prepare the response data and sort by year and month in descending order (recent first)
        report = []
        for (year, month), data in sorted(monthly_data.items(), reverse=True):
            report.append({
                'year': year,
                'month': date(year, month, 1).strftime('%B'),  # Convert month number to name
                'credit': float(data['credit']),  # Convert Decimal to float for the response
                'debit': float(data['debit']),
                'balance': float(data['balance']),
            })

        return Response({
            'status': 'success',
            'message': 'Monthly transaction report generated successfully',
            'data': report,
        }, status=status.HTTP_200_OK)

################################################## ACCOUNT OVERVIEW ##################################################

class AccountsOverview(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        bank_accounts = Account.objects.filter(user=request.user)
        accounts = []

        for bank_account in bank_accounts:
            credited = Transaction.objects.filter(user=request.user,account=bank_account, type='credit').aggregate(Sum('amount'))['amount__sum'] or 0
            debited = Transaction.objects.filter(user=request.user,account=bank_account, type='debit').aggregate(Sum('amount'))['amount__sum'] or 0
            credit_transfer = SelfTransfer.objects.filter(user=request.user,to_account=bank_account).aggregate(Sum('amount'))['amount__sum'] or 0
            debit_transfer = SelfTransfer.objects.filter(user=request.user,from_account=bank_account).aggregate(Sum('amount'))['amount__sum'] or 0

            balance = (credited - debited + credit_transfer) - debit_transfer

            account = {
                'name': bank_account.name,
                'bank': bank_account.bank,

                'credited': credited,
                'debited': debited,
                'credit_transfer': credit_transfer,
                'debit_transfer' : debit_transfer,

                'balance': balance,
            }

            accounts.append(account)

        return Response({
            'status': 'success',
            'message': 'Account overview retrieved successfully',
            'data': accounts,
        }, status=status.HTTP_200_OK)

################################################## TRANSACTIONS LIST & CREATE ##################################################

class TransactionList(generics.ListCreateAPIView):
    serializer_class = TransactionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TransactionFilter
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        transactions = self.filter_queryset(self.get_queryset())

        credited = transactions.filter(type='credit').exclude(account__type='savings_account').aggregate(total_amount=Sum('amount'))['total_amount'] or 0.0
        debited = transactions.filter(type='debit').exclude(account__type='savings_account').aggregate(total_amount=Sum('amount'))['total_amount'] or 0.0

        to_savings_account = SelfTransfer.objects.filter(user=request.user,to_account__type='savings_account').aggregate(total_amount=Sum('amount'))['total_amount'] or 0.0
        from_savings_account = SelfTransfer.objects.filter(user=request.user,from_account__type='savings_account').aggregate(total_amount=Sum('amount'))['total_amount'] or 0.0

        to_other_accounts = SelfTransfer.objects.filter(user=request.user).exclude(to_account__type='savings_account').aggregate(total_amount=Sum('amount'))['total_amount'] or 0.0
        from_other_accounts = SelfTransfer.objects.filter(user=request.user).exclude(from_account__type='savings_account').aggregate(total_amount=Sum('amount'))['total_amount'] or 0.0

        balance = ((credited - debited) - to_savings_account) + from_savings_account

        credited_to_savings = transactions.filter(account__type='savings_account', type='credit').aggregate(total_amount=Sum('amount'))['total_amount'] or 0.0
        debited_from_savings = transactions.filter(account__type='savings_account', type='debit').aggregate(total_amount=Sum('amount'))['total_amount'] or 0.0

        savings = (to_savings_account + credited_to_savings) - debited_from_savings - from_savings_account

        serializer = self.get_serializer(transactions, many=True)

        return Response({
            'status': 'success',
            'message': 'Transactions retrieved successfully',
            'data': serializer.data,
            'credited': credited,
            'debited': debited,
            'balance': balance,
            'savings': savings
        }, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)
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


################################################## TRANSACTIONS UPDATE & DELETE ##################################################

class TransactionDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

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

################################################## SELF TRANSFER LIST & CREATE ##################################################

class SelfTransferList(generics.ListCreateAPIView):
    serializer_class = SelfTransferSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SelfTransfer.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        transfers = self.filter_queryset(self.get_queryset())

        serializer = self.get_serializer(transfers, many=True)

        return Response({
            'status': 'success',
            'message': 'Self Transfers retrieved successfully',
            'data': serializer.data,
        }, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({
                'status': 'success',
                'message': 'Self transfer created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            'status': 'error',
            'message': 'Failed to create self transfer',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

################################################## SELF TRANSFER UPDATE & DELETE ##################################################

class SelfTransferDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SelfTransferSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SelfTransfer.objects.filter(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return Response({
            'status': 'success',
            'message': 'Self transfer retrieved successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response({
                'status': 'success',
                'message': 'Self transfer updated successfully',
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
            'message': 'Self transfer deleted successfully'
        }, status=status.HTTP_200_OK)

################################################## TASK LIST & CREATE ##################################################

class TaskList(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TaskFilter
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

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
            order_id = Task.objects.last().order + 1 if Task.objects.exists() else 1
            serializer.save(order=order_id)
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

################################################## TASK UPDATE & DELETE ##################################################

class TaskDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

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

################################################## TASK ORDER UPDATE ##################################################

class TaskOrderUpdate(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    
    def update(self, request, *args, **kwargs):
        try:
            task_orders = request.data.get('task_orders', [])
            
            for order_data in task_orders:
                task = Task.objects.get(id=order_data['id'])
                task.order = order_data['order']
                task.save()
                
            return Response({
                'status': 'success',
                'message': 'Task order updated successfully'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

################################################## TODO LIST & CREATE ##################################################

class TodoList(generics.ListCreateAPIView):
    serializer_class = TodoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TodoFilter
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)

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
            serializer.save(user=request.user)
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

################################################## TODO UPDATE & DELETE ##################################################

class TodoDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)

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

################################################## CHECKLIST ##################################################

class CheckList(generics.ListCreateAPIView):
    serializer_class = ChecklistItemSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ChecklistItemFilter
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ChecklistItem.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(date=today)

        if not queryset.exists():
            tasks = Task.objects.all().order_by('order')
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

################################################## CHECKLIST DETAILS ##################################################

class CheckListDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ChecklistItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ChecklistItem.objects.filter(user=self.request.user)

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

################################################## PREVIOUS DAYS ##################################################

class PreviousDays(APIView):
    def get(self, request, *args, **kwargs):
        dates = sorted(set(ChecklistItem.objects.values_list('date', flat=True)), reverse=True)
        data = []

        for date in dates:
            tasks = ChecklistItem.objects.filter(user=request.user,date=date)
            completed = tasks.filter(completed=False).count() == 0

            data.append({'date': date, 'completed': completed})

        return Response({
            'status': 'success',
            'message': 'Dates retrieved successfully',
            'data': data
        }, status=status.HTTP_200_OK)

################################################## PREVIOUS DAY TASKS ##################################################

class PreviousDayTasks(generics.ListAPIView):
    queryset = ChecklistItem.objects.all()
    serializer_class = ChecklistItemSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ChecklistItemFilter
    ordering_fields = ['date']

################################################## JOURNAL LIST & CREATE ##################################################

class JournalList(generics.ListCreateAPIView):
    serializer_class = JournalSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = JournalFilter
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Journal.objects.filter(user=self.request.user)

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
            serializer.save(user=request.user)
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

################################################## JOURNAL UPDATE & DELETE ##################################################

class JournalDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = JournalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Journal.objects.filter(user=self.request.user)

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