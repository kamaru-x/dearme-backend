# Generated by Django 4.2.7 on 2024-12-01 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_transaction_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='priority',
            field=models.CharField(choices=[('high', 'High'), ('normal', 'Normal'), ('low', 'Low')], default='normal', max_length=10),
        ),
        migrations.AlterField(
            model_name='todo',
            name='title',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
