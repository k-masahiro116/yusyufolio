# Generated by Django 4.1.2 on 2023-09-26 09:44

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('speaker', models.CharField(max_length=200, verbose_name='話者')),
                ('text', models.TextField(verbose_name='本文')),
                ('date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='日付')),
            ],
        ),
    ]
