# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2020-05-04 17:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0013_auto_20200504_2149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='images',
            name='image',
            field=models.ImageField(blank=True, height_field='height_field', null=True, upload_to='images/', width_field='width_field'),
        ),
    ]