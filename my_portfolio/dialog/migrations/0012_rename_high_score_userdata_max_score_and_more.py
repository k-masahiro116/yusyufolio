# Generated by Django 4.1.2 on 2023-12-22 10:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dialog', '0011_alter_userdata_hdsr'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userdata',
            old_name='high_score',
            new_name='max_score',
        ),
        migrations.RenameField(
            model_name='userdata',
            old_name='row_score',
            new_name='min_score',
        ),
    ]
