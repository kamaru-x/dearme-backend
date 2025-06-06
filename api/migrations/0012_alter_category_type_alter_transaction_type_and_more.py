# Generated by Django 5.1.4 on 2025-01-04 04:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_alter_account_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='type',
            field=models.CharField(choices=[('credit', 'Credit'), ('debit', 'Debit')], max_length=25),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='type',
            field=models.CharField(choices=[('credit', 'Credit'), ('debit', 'Debit')], max_length=25),
        ),
        migrations.CreateModel(
            name='SelfTransfer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('amount', models.FloatField()),
                ('from_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_account', to='api.account')),
                ('to_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_account', to='api.account')),
            ],
            options={
                'ordering': ['-date', '-id'],
                'indexes': [models.Index(fields=['-date', '-id'], name='api_selftra_date_2a495a_idx')],
            },
        ),
    ]
