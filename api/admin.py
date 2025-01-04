from django.contrib import admin
from .models import Account, Category, Transaction, SelfTransfer, Todo, Task, ChecklistItem, Journal

# Register your models here.
class AccountAdmin(admin.ModelAdmin):
    list_display = ['name', 'bank', 'number', 'date']
    search_fields = ['name', 'bank', 'number']
    list_filter = ['date', 'bank']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'date']
    search_fields = ['name']
    list_filter = ['type', 'date']

class TransactionAdmin(admin.ModelAdmin):
    list_display = ['title', 'type', 'account', 'category', 'amount', 'date']
    search_fields = ['title', 'account__name', 'category__name']
    list_filter = ['type', 'date', 'account', 'category']


class SelfTransferAdmin(admin.ModelAdmin):
    list_display = ['from_account', 'to_account', 'amount', 'date']
    search_fields = ['from_account__name', 'to_account__name']
    list_filter = ['date']


class TodoAdmin(admin.ModelAdmin):
    list_display = ['title', 'priority', 'completed', 'date']
    search_fields = ['title']
    list_filter = ['priority', 'completed', 'date']

class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'date']
    search_fields = ['title']
    list_filter = ['date']

class ChecklistItemAdmin(admin.ModelAdmin):
    list_display = ['task', 'date', 'completed']
    search_fields = ['task__title']
    list_filter = ['completed', 'date']

class JournalAdmin(admin.ModelAdmin):
    list_display = ['title', 'mood', 'date']
    search_fields = ['title', 'content']
    list_filter = ['mood', 'date']

admin.site.register(Account, AccountAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Todo, TodoAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(ChecklistItem, ChecklistItemAdmin)
admin.site.register(Journal, JournalAdmin)
admin.site.register(SelfTransfer, SelfTransferAdmin)