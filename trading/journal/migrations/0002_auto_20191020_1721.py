# Generated by Django 2.2.6 on 2019-10-20 17:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lesson',
            name='external_link',
        ),
        migrations.RemoveField(
            model_name='lesson',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='reason',
            name='external_link',
        ),
        migrations.RemoveField(
            model_name='reason',
            name='owner',
        ),
    ]