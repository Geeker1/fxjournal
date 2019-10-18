# Generated by Django 2.2.6 on 2019-10-17 09:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('journal', '0004_auto_20191017_0859'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ImageContent',
            new_name='Image',
        ),
        migrations.RenameModel(
            old_name='TextContent',
            new_name='Text',
        ),
        migrations.AlterField(
            model_name='content',
            name='content_type',
            field=models.ForeignKey(limit_choices_to={'model__in': ('image', 'text')}, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType'),
        ),
    ]
