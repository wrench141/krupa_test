# Generated by Django 5.1 on 2024-11-01 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('krupa', '0025_alter_estimate_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='salesorder',
            name='satus',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]