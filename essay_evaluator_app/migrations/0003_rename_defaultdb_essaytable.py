# Generated by Django 4.2.11 on 2024-04-13 10:31

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('essay_evaluator_app', '0002_rename_essaytable_defaultdb'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='defaultdb',
            new_name='EssayTable',
        ),
    ]
