# Generated by Django 5.2 on 2025-04-18 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_approved',
        ),
        migrations.AddField(
            model_name='accountapplication',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
    ]
