import django_filters
from .models import Account, Category, Transaction, Todo, Task, ChecklistItem, Journal

class AccountFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    bank = django_filters.CharFilter(lookup_expr='icontains')
    date = django_filters.DateFilter()

    class Meta:
        model = Account
        fields = ['name', 'bank', 'number', 'date']

class CategoryFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    type = django_filters.ChoiceFilter(choices=[('credit', 'Credit'), ('debit', 'Debit')])
    date = django_filters.DateFilter()

    class Meta:
        model = Category
        fields = ['name', 'type', 'date']

class TransactionFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    type = django_filters.ChoiceFilter(choices=[('credit', 'Credit'), ('debit', 'Debit')])
    account = django_filters.ModelChoiceFilter(queryset=Account.objects.all())
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.all())
    amount_min = django_filters.NumberFilter(field_name='amount', lookup_expr='gte')
    amount_max = django_filters.NumberFilter(field_name='amount', lookup_expr='lte')
    date = django_filters.DateFilter()
    from_date = django_filters.DateFilter(field_name='date', lookup_expr='gte')
    to_date = django_filters.DateFilter(field_name='date', lookup_expr='lte')

    class Meta:
        model = Transaction
        fields = ['title', 'type', 'account', 'category', 'amount', 'date']
        order_by = ['-date', '-id']  # Default ordering by date descending, then id descending

class TodoFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    priority = django_filters.ChoiceFilter(choices=[('high', 'High'), ('medium', 'Medium'), ('low', 'Low')])
    completed = django_filters.BooleanFilter()
    date = django_filters.DateFilter()

    class Meta:
        model = Todo
        fields = ['title', 'priority', 'completed', 'date']

class TaskFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    date = django_filters.DateFilter()
    order = django_filters.NumberFilter()

    class Meta:
        model = Task
        fields = ['title', 'date', 'order']

class ChecklistItemFilter(django_filters.FilterSet):
    task = django_filters.ModelChoiceFilter(queryset=Task.objects.all())
    completed = django_filters.BooleanFilter()
    date = django_filters.DateFilter()

    class Meta:
        model = ChecklistItem
        fields = ['task', 'completed', 'date']

class JournalFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    mood = django_filters.ChoiceFilter(choices=[('happy', 'Happy'), ('neutral', 'Neutral'), ('sad', 'Sad')])
    content = django_filters.CharFilter(lookup_expr='icontains')
    date = django_filters.DateFilter()

    class Meta:
        model = Journal
        fields = ['title', 'mood', 'content', 'date']
