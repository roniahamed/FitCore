# Generated by Django 5.2.3 on 2025-07-16 08:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchases',
            name='user',
        ),
        migrations.RemoveField(
            model_name='subscriptions',
            name='user',
        ),
        migrations.DeleteModel(
            name='Payments',
        ),
        migrations.DeleteModel(
            name='Purchases',
        ),
        migrations.DeleteModel(
            name='Subscriptions',
        ),
    ]
