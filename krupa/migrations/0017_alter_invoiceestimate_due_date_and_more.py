# Generated by Django 5.1 on 2024-10-23 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('krupa', '0016_invoiceestimate_item'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoiceestimate',
            name='due_date',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='invoiceestimate',
            name='invoice_date',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
