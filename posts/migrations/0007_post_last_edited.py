# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2020-05-04 01:48
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_auto_20200503_1751'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='last_edited',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2020, 5, 4, 1, 48, 25, 283191, tzinfo=utc)),
            preserve_default=False,
        ),
    ]