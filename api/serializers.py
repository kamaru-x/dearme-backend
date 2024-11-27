from rest_framework import serializers
from .models import Account, Category, Transaction, Todo, Task, ChecklistItem, Journal

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'date', 'name', 'bank', 'number']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'date', 'type', 'name']

class TransactionSerializer(serializers.ModelSerializer):
    account_name = serializers.CharField(source='account.name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Transaction
        fields = ['id', 'date', 'title', 'type', 'account', 'account_name', 'category', 'category_name', 'amount']

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ['id', 'date', 'title', 'priority', 'completed']

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'date', 'title']

class ChecklistItemSerializer(serializers.ModelSerializer):
    task_title = serializers.CharField(source='task.title', read_only=True)

    class Meta:
        model = ChecklistItem
        fields = ['id', 'task', 'task_title', 'date', 'completed']

class JournalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Journal
        fields = ['id', 'date', 'title', 'mood', 'content']