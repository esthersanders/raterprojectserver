# Generated by Django 3.1.3 on 2020-11-06 16:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('raterprojectapi', '0003_player'),
    ]

    operations = [
        migrations.RenameField(
            model_name='game',
            old_name='user',
            new_name='player',
        ),
    ]
