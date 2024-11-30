from django.db import models

# Create your models here.

TYPES = (
    ('credit', 'Credit'),
    ('debit', 'Debit'),
)

PRIORITY = (
    ('high', 'High'),
    ('medium', 'Medium'),
    ('low', 'Low'),
)

MOOD = (
    ('happy', 'Happy'),
    ('neutral', 'Neutral'),
    ('sad', 'Sad'),
)

class Account(models.Model):
    date = models.DateField(auto_now_add=True)
    name = models.CharField(max_length=100)
    bank = models.CharField(max_length=100)
    number = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Category(models.Model):
    date = models.DateField(auto_now_add=True)
    type = models.CharField(max_length=10, choices=TYPES)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Transaction(models.Model):
    date = models.DateField()
    title = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=TYPES)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.category.name} - {self.amount}"

class Todo(models.Model):
    date = models.DateField(auto_now_add=True)
    title = models.CharField(max_length=100)
    priority = models.CharField(max_length=10, choices=PRIORITY)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Task(models.Model):
    date = models.DateField(auto_now_add=True)
    title = models.CharField(max_length=100)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class ChecklistItem(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    date = models.DateField()
    completed = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.task.title} - {self.date}"

class Journal(models.Model):
    date = models.DateField(auto_now_add=True)
    title = models.CharField(max_length=100)
    mood = models.CharField(max_length=50,choices=MOOD)
    content = models.TextField()

    def __str__(self):
        return self.title