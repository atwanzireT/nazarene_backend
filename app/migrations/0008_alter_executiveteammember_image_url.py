# Generated by Django 5.2 on 2025-05-18 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_contactmessage_executiveteammember'),
    ]

    operations = [
        migrations.AlterField(
            model_name='executiveteammember',
            name='image_url',
            field=models.ImageField(default='placeholder.jpg', upload_to='staff'),
        ),
    ]
