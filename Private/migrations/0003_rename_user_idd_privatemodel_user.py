# Generated by Django 4.1 on 2023-06-14 07:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Private', '0002_privatemodel_user_idd'),
    ]

    operations = [
        migrations.RenameField(
            model_name='privatemodel',
            old_name='user_idd',
            new_name='user',
        ),
    ]
