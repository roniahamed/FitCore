from django.db import models
from django.conf import settings
from django.utils import timezone
from dateutil.relativedelta import relativedelta


class PlanType(models.TextChoices):
    """Defines the available plans. This is static as you have only two types."""
    MONTHLY = 'MONTHLY', 'Monthly Subscription'
    LIFETIME = 'LIFETIME', 'Lifetime Access (One-Time)'





class Subscriptions(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subscriptions')
    plan_type = models.CharField(max_length=100, help_text="Type of subscription plan (e.g., Basic, Premium)")
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    status = models.CharField(max_length=50, help_text="Subscription status (e.g., Active, Inactive, Cancelled)")

    def __str__(self):
        return f"{self.user.username}'s {self.plan_type} Subscription"
    
    class Meta:
        verbose_name = 'Subscription'
        verbose_name_plural = 'Subscriptions'
        ordering = ['-start_date']


class Payments(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payments')
    subscription = models.ForeignKey(Subscriptions, on_delete=models.SET_NULL, null=True, blank=True, related_name='payments')
    plan_name = models.CharField(max_length=200, blank=False, null=False, help_text="Name of the plan at the time of purchase")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, help_text="Payment status (e.g., Succeeded, Failed, Pending)")
    plan_type = models.CharField(max_length=100, blank=False, null=False, help_text="Type of plan purchased (e.g., Basic, Premium)")
    start_date = models.DateTimeField(help_text="Subscription start date related to this payment")
    end_date = models.DateTimeField(help_text="Subscription end date related to this payment")
    purchases_date = models.DateTimeField(help_text="Date and time of the purchase")

    def __str__(self):
        return f"Payment of {self.amount} by {self.user.email} on {self.purchase_date.strftime('%Y-%m-%d')}"
    
    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'
        ordering = ['-purchases_date']


class Purchases(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='purchases')
    plan_type = models.CharField(max_length=100)
    purchases_date = models.DateField()
    transaction_id = models.CharField(max_length=200)
    
    def __str__(self):
        return f"{self.user} - {self.plan_type}"
