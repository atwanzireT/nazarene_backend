# Generated by Django 5.2 on 2025-05-18 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_activity_status_event_status_alter_project_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('subject', models.CharField(blank=True, max_length=255)),
                ('message', models.TextField()),
                ('category', models.CharField(choices=[('general', 'General Inquiry'), ('alumni', 'Alumni Support'), ('events', 'Events & Programming'), ('donations', 'Donations & Giving'), ('careers', 'Career Services')], default='general', max_length=20)),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ExecutiveTeamMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone', models.CharField(max_length=20)),
                ('term_start', models.DateField()),
                ('term_end', models.DateField()),
                ('image_url', models.URLField(default='placeholder.jpg')),
            ],
        ),
    ]
