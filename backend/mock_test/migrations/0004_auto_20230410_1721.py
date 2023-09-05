# Generated by Django 3.2 on 2023-04-10 17:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0011_auto_20230410_1718'),
        ('mock_test', '0003_auto_20230410_1714'),
    ]

    operations = [
        migrations.AddField(
            model_name='mocktest',
            name='questions',
            field=models.ManyToManyField(blank=True, to='questions.GREQuestion'),
        ),
        migrations.AddField(
            model_name='questioninteraction',
            name='question',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='questions.grequestion'),
        ),
    ]
