# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-23 21:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('departures', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='departure',
            name='track',
            field=models.IntegerField(null=True),
        ),
    ]
