# Generated by Django 2.2 on 2020-09-15 12:24

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_auto_20200915_1753'),
    ]

    operations = [
        migrations.AddField(
            model_name='adduserprofile',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
