from django.db.models.signals import post_save 
from django.dispatch import receiver
from .models import UsersProfile, CustomUser


@receiver(post_save, CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UsersProfile.objects.create(user = instance)