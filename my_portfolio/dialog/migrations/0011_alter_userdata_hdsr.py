# Generated by Django 4.1.2 on 2023-12-22 04:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dialog', '0010_remove_userdata_hdsr_userdata_hdsr'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdata',
            name='hdsr',
            field=models.ManyToManyField(blank=True, null=True, to='dialog.hdsr_model', verbose_name='HDS-R'),
        ),
    ]
