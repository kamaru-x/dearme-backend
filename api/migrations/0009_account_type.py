# Generated by Django 5.1.4 on 2025-01-03 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_alter_category_type_alter_transaction_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='type',
            field=models.CharField(choices=[('savings', 'Savings'), ('slary_account', 'Slary Account'), ('primary_account', 'Primary Account'), ('secondary_account', 'Secondary Account')], default=1, max_length=50),
            preserve_default=False,
        ),
    ]
