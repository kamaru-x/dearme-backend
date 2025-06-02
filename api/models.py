from django.db import models

# Create your models here.

TYPES = (
    ('credit', 'Credit'),
    ('debit', 'Debit')
)

PRIORITY = (
    ('high', 'High'),
    ('normal', 'Normal'),
    ('low', 'Low'),
)

MOOD = (
    ('happy', 'Happy'),
    ('neutral', 'Neutral'),
    ('sad', 'Sad'),
)

ACCOUNT_TYPE = (
    ('primary_account', 'Primary Account'),
    ('secondary_account', 'Secondary Account'),
    ('savings_account', 'Savings Account'),
)

class Account(models.Model):
    date = models.DateField(auto_now_add=True)
    type = models.CharField(max_length=50, choices=ACCOUNT_TYPE)
    name = models.CharField(max_length=100)
    bank = models.CharField(max_length=100)
    number = models.CharField(max_length=100, default='XXXXXXXXXXXX')

    def __str__(self):
        return self.name

class Category(models.Model):
    date = models.DateField(auto_now_add=True)
    type = models.CharField(max_length=25, choices=TYPES)
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['type', 'date', 'id']
        indexes = [
            models.Index(fields=['type', 'date', 'id']),
        ]

    def __str__(self):
        return self.name

class Transaction(models.Model):
    date = models.DateField()
    title = models.CharField(max_length=100)
    type = models.CharField(max_length=25, choices=TYPES)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.FloatField()

    class Meta:
        ordering = ['-date', '-id']
        indexes = [
            models.Index(fields=['-date', '-id']),
        ]

    def __str__(self):
        return f"{self.category.name} - {self.amount}"


class SelfTransfer(models.Model):
    date = models.DateField(auto_now_add=True)
    from_account = models.ForeignKey(Account, related_name='from_account', on_delete=models.CASCADE)
    to_account = models.ForeignKey(Account, related_name='to_account', on_delete=models.CASCADE)
    amount = models.FloatField()

    def __str__(self):
        return f"{self.from_account.name} -> {self.to_account.name} - {self.amount}"

    class Meta:
        ordering = ['-date', '-id']
        indexes = [
            models.Index(fields=['-date', '-id']),
        ]


class Todo(models.Model):
    date = models.DateField(auto_now_add=True)
    title = models.CharField(max_length=100,null=True)
    priority = models.CharField(max_length=10, choices=PRIORITY, default='normal')
    completed = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date', '-id']
        indexes = [
            models.Index(fields=['-date', '-id']),
        ]

    def __str__(self):
        return self.title

class Task(models.Model):
    date = models.DateField(auto_now_add=True)
    title = models.CharField(max_length=100)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', '-date', '-id']
        indexes = [
            models.Index(fields=['order', '-date', '-id']),
        ]

    def __str__(self):
        return self.title

class ChecklistItem(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    date = models.DateField()
    completed = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date', '-id']
        indexes = [
            models.Index(fields=['-date', '-id']),
        ]

    def __str__(self):
        return f"{self.task.title} - {self.date}"

class Journal(models.Model):
    date = models.DateField()
    title = models.CharField(max_length=100)
    mood = models.CharField(max_length=50,choices=MOOD)
    content = models.TextField()

    class Meta:
        ordering = ['-date', '-id']
        indexes = [
            models.Index(fields=['-date', '-id']),
        ]

    def __str__(self):
        return self.title