# Generated by Django 3.2 on 2023-04-08 17:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mock_test', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mocktest',
            name='subjects',
        ),
    ]