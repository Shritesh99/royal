# Generated by Django 3.2 on 2023-03-30 14:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fslsmquestion',
            name='choices',
        ),
        migrations.RemoveField(
            model_name='grequestion',
            name='answer',
        ),
        migrations.RemoveField(
            model_name='grequestion',
            name='choices',
        ),
        migrations.RemoveField(
            model_name='grequestion',
            name='tags',
        ),
        migrations.DeleteModel(
            name='Choice',
        ),
        migrations.DeleteModel(
            name='FSLSMQuestion',
        ),
        migrations.DeleteModel(
            name='GREQuestion',
        ),
    ]
