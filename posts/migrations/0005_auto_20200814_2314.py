# Generated by Django 2.2 on 2020-08-14 17:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_user_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='image',
        ),
        migrations.RemoveField(
            model_name='user',
            name='isStaff',
        ),
    ]
