# Generated by Django 3.2 on 2023-04-14 02:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_remove_appuser_motivation'),
    ]

    operations = [
        migrations.AddField(
            model_name='appuser',
            name='motivation',
            field=models.FloatField(default=0, null=True),
        ),
    ]