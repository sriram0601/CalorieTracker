# Generated by Django 3.1.7 on 2021-08-06 15:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CalorieApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
