# Generated by Django 5.1 on 2024-10-25 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('krupa', '0022_salesorder_created_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='estimate',
            name='created_date',
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name='invoiceestimate',
            name='created_date',
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='created_date',
            field=models.DateField(auto_now=True),
        ),
    ]
