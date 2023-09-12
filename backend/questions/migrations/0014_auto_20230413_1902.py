# Generated by Django 3.2 on 2023-04-13 19:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0013_motivationquestion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='motivationquestion',
            name='choices',
        ),
        migrations.CreateModel(
            name='MotivationInteraction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.IntegerField(default=0)),
                ('question', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='questions.motivationquestion')),
            ],
        ),
    ]