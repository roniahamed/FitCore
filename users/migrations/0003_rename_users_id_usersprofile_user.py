# Generated by Django 5.2.1 on 2025-05-25 05:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_usersprofile'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usersprofile',
            old_name='users_id',
            new_name='user',
        ),
    ]
