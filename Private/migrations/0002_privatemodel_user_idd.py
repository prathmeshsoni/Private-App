# Generated by Django 4.1 on 2023-06-14 07:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Private', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='privatemodel',
            name='user_idd',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
