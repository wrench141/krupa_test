# Generated by Django 5.1 on 2024-11-11 14:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('krupa', '0041_expense_recurringexpense'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='estimate',
            field=models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, to='krupa.estimate'),
            preserve_default=False,
        ),
    ]
