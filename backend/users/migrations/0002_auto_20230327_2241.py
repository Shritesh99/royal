# Generated by Django 3.2 on 2023-03-27 22:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('social_django', '0013_delete_socialauth'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='appuser',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='social_auth_profiles', to='social_django.usersocialauth'),
        ),
        migrations.AlterField(
            model_name='appuser',
            name='dob',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='appuser',
            name='gender',
            field=models.CharField(default='male', max_length=6, null=True),
        ),
    ]
