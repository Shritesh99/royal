# Generated by Django 3.2 on 2023-04-08 17:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0004_auto_20230408_0320'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Goal',
        ),
        migrations.RemoveField(
            model_name='grequestion',
            name='answer',
        ),
    ]
