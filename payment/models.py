from django.db import models
from django.conf import settings
from django.utils import timezone
from dateutil.relativedelta import relativedelta


class PlanType(models.TextChoices):
    """Defines the available plans. This is static as you have only two types."""
    MONTHLY = 'MONTHLY', 'Monthly Subscription'
    LIFETIME = 'LIFETIME', 'Lifetime Access (One-Time)'

class PaymentGateway(models.TextChoices):
    """Kept as choices as you might add PayPal later, but it's simple."""
    STRIPE = 'STRIPE', 'Stripe'
    PAYPAL = 'PAYPAL', 'Paypal'
    MANUAL = 'MANUAL', 'Manual/Admin'

class PaymentStatus(models.TextChoices):
    """ Tracks the status of each payment attempt. """
    PENDING = 'PENDING', 'Pending'
    SUCCEEDED = 'SUCCEEDED', 'Succeeded'
    FAILED = 'FAILED', 'Failed'
    REFUNDED = 'REFUNDED', 'Refunded'

class SubscriptionStatus(models.TextChoices):
    """Tracks the user's overall access status."""
    ACTIVE = 'ACTIVE', 'Active'
    INACTIVE = 'INACTIVE', 'Inactive' # When a monthly plan expires
    CANCELLED = 'CANCELLED', 'Cancelled' # User cancelled monthly, active until period end
    PAST_DUE = 'PAST_DUE', 'Past Due' # Monthly payment failed

# --- Core Models ---

class Subscription(models.Model):
    """
    Stores the user's current access plan and status.
    There will be only one active subscription per user.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,  related_name='subscription',
        primary_key=True # A user can have only one subscription record, making this a profile extension
    )
    plan = models.CharField(
        max_length=20,
        choices=PlanType.choices,
        help_text="The plan the user is currently on."
    )
    status = models.CharField(
        max_length=20,
        choices=SubscriptionStatus.choices,
        default=SubscriptionStatus.INACTIVE
    )
    start_date = models.DateTimeField(
        null=True, blank=True,
        help_text="Date when the subscription first started or the current period began."
    )
    end_date = models.DateTimeField(
        null=True, blank=True,
        help_text="For MONTHLY plan, this is the end of the current billing cycle. For LIFETIME, this is null."
    )

    # --- Gateway Specific Subscription Info (for recurring payments) ---
    gateway = models.CharField(max_length=20, choices=PaymentGateway.choices, null=True, blank=True)
    gateway_subscription_id = models.CharField(
        max_length=255, unique=True, null=True, blank=True,
        help_text="e.g., Stripe Subscription ID (sub_...). Only for MONTHLY plan."
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s {self.get_plan_display()} Plan ({self.get_status_display()})"
    

    @property
    def has_active_access(self):
        """A single property to check if the user should have access."""
        if self.plan == PlanType.LIFETIME and self.status == SubscriptionStatus.ACTIVE:
            return True
        if self.plan == PlanType.MONTHLY and self.status == SubscriptionStatus.ACTIVE and self.end_date and self.end_date > timezone.now():
            return True
        return False
        
    class Meta:
        verbose_name = 'User Subscription'
        verbose_name_plural = 'User Subscriptions'



