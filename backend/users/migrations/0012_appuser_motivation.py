# Generated by Django 3.2 on 2023-04-13 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0014_auto_20230413_1902'),
        ('users', '0011_appuser_is_first_test'),
    ]

    operations = [
        migrations.AddField(
            model_name='appuser',
            name='motivation',
            field=models.ManyToManyField(blank=True, to='questions.MotivationInteraction'),
        ),
    ]