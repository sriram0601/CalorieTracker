# Generated by Django 3.1.7 on 2021-08-07 03:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CalorieApp', '0002_auto_20210806_2115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='date',
            field=models.DateTimeField(default=datetime.date(2021, 8, 7)),
        ),
    ]
