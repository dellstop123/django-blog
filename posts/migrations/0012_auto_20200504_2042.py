# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2020-05-04 15:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0011_images'),
    ]

    operations = [
        migrations.AddField(
            model_name='images',
            name='height_field',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='images',
            name='width_field',
            field=models.IntegerField(default=0),
        ),
    ]
