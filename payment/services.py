from django.utils import timezone
from dateutil.relativedelta import relativedelta
from .models import Subscription, PlanType, SubscriptionStatus


def activate_user_subscription(user, plan_type, gateway, gateway_subscription_id=None):
    """
    Activates or updates a user's subscription based on a successful payment.
    This function is designed to be called from a webhook handler.
    """
    subscription, created = Subscription.objects.get_or_create(user=user)
    subscription.plan = plan_type
    subscription.status = SubscriptionStatus.ACTIVE
    subscription.gateway = gateway

    if plan_type == PlanType.MONTHLY:
        # If it's a renewal, the start date might already be set.
        # For a new subscription, set the start date.
        if created or not subscription.start_date:
            subscription.start_date = timezone.now()
        subscription.end_date = timezone.now() + relativedelta(months=1)
        subscription.gateway_subscription_id = gateway_subscription_id
    elif plan_type == PlanType.LIFETIME:
        subscription.start_date = timezone.now()
        subscription.end_date = None
        subscription.gateway_subscription_id = None
    subscription.save()
    return subscription

def handle_subscription_cancellation(gateway_subscription_id):
    """
    Handles a subscription cancellation event from the gateway.
    """
    try:
        subscription = Subscription.objects.get(gateway_subscription_id=gateway_subscription_id)
        subscription.status = SubscriptionStatus.CANCELLED
        # Note: end_date remains the same. The user has access until the period ends.
        subscription.save()
    except Subscription.DoesNotExist:
         # Log this error: A cancellation webhook was received for a subscription not in our DB.
        print(f"Subscription with gateway_id {gateway_subscription_id} not found.")