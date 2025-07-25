# Generated by Django 5.2.3 on 2025-07-17 06:43

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0004_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan_at_purchase', models.CharField(choices=[('MONTHLY', 'Monthly Subscription'), ('LIFETIME', 'Lifetime Access (One-Time)')], max_length=20)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('currency', models.CharField(default='USD', max_length=3)),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('SUCCEEDED', 'Succeeded'), ('FAILED', 'Failed'), ('REFUNDED', 'Refunded')], default='PENDING', max_length=20)),
                ('gateway', models.CharField(choices=[('STRIPE', 'Stripe'), ('PAYPAL', 'Paypal'), ('MANUAL', 'Manual/Admin')], max_length=20)),
                ('gateway_transaction_id', models.CharField(max_length=255, unique=True)),
                ('invoice_url', models.URLField(blank=True, null=True)),
                ('gateway_response', models.JSONField(blank=True, null=True)),
                ('transaction_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transactions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Transaction',
                'verbose_name_plural': 'Transactions',
                'ordering': ['-transaction_date'],
            },
        ),
    ]
