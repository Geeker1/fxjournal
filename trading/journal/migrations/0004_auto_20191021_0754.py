# Generated by Django 2.2.6 on 2019-10-21 07:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0003_auto_20191021_0751'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lesson',
            name='l_image',
        ),
        migrations.RemoveField(
            model_name='lesson',
            name='l_text',
        ),
        migrations.RemoveField(
            model_name='reason',
            name='r_image',
        ),
        migrations.RemoveField(
            model_name='reason',
            name='r_text',
        ),
    ]