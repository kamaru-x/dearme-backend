from rest_framework import serializers
from .models import Account, Category, Transaction, Todo, Task, ChecklistItem, Journal

class AccountSerializer(serializers.ModelSerializer):
    type_value = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = ['id', 'date', 'name', 'bank', 'type', 'type_value']

    def get_type_value(self, obj):
        return obj.get_type_display()

class CategorySerializer(serializers.ModelSerializer):
    type_value = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'date', 'type', 'type_value', 'name']

    def get_type_value(self, obj):
        return obj.get_type_display()

class TransactionSerializer(serializers.ModelSerializer):
    account_name = serializers.CharField(source='account.name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    type_value = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = ['id', 'date', 'title', 'type', 'type_value', 'account', 'account_name', 'category', 'category_name', 'amount']

    def get_type_value(self, obj):
        return obj.get_type_display()

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


class DashboardSerializer(serializers.Serializer):
    accounts = AccountSerializer(many=True)
    categories = CategorySerializer(many=True)
    transactions = TransactionSerializer(many=True)
    todos = TodoSerializer(many=True)
    tasks = TaskSerializer(many=True)
    checklist_items = ChecklistItemSerializer(many=True)
    journals = JournalSerializer(many=True)