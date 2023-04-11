# Generated by Django 3.2 on 2023-04-10 17:03

from django.db import migrations, models
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0005_auto_20220424_2025'),
        ('questions', '0006_alter_grequestion_difficulty'),
    ]

    operations = [
        migrations.CreateModel(
            name='FSLSMChoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
            ],
            options={
                'verbose_name': 'FSLSM Choice',
                'verbose_name_plural': 'FSLSM Choices',
            },
        ),
        migrations.AlterField(
            model_name='grequestion',
            name='subjects',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='questions.Subject', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.AlterField(
            model_name='fslsmquestion',
            name='choices',
            field=models.ManyToManyField(blank=True, to='questions.FSLSMChoice'),
        ),
    ]