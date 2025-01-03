# Generated by Django 5.1.4 on 2025-01-03 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_alter_checklistitem_options_alter_journal_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='type',
            field=models.CharField(choices=[('credit', 'Credit'), ('debit', 'Debit'), ('transfer', 'Transfer')], max_length=10),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='type',
            field=models.CharField(choices=[('credit', 'Credit'), ('debit', 'Debit'), ('transfer', 'Transfer')], max_length=10),
        ),
    ]
