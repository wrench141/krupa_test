# Generated by Django 5.1 on 2024-11-26 09:19

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('krupa', '0064_request_shipping_alter_shippingaddress_request'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shippingaddress',
            name='request',
        ),
        migrations.AddField(
            model_name='shippingaddress',
            name='profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='request',
            name='shipping',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='krupa.shippingaddress'),
        ),
    ]
