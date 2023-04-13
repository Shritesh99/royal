# Generated by Django 3.2 on 2023-04-08 03:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mock_test', '0001_initial'),
        ('users', '0009_auto_20230328_0249'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInteraction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField()),
                ('login_timestamp', models.DateTimeField()),
                ('time_spent_today', models.IntegerField()),
                ('total_questions_today', models.IntegerField()),
                ('accuracy_today', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='UserPerformance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avg_accuracy', models.FloatField()),
                ('avg_time', models.IntegerField()),
                ('avg_question_daily', models.IntegerField()),
                ('total_score', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='appuser',
            name='mock_tests',
            field=models.ManyToManyField(blank=True, to='mock_test.MockTest'),
        ),
        migrations.AddField(
            model_name='appuser',
            name='user_interaction',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.userinteraction'),
        ),
        migrations.AddField(
            model_name='appuser',
            name='user_performance',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.userperformance'),
        ),
    ]