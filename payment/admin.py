from django.contrib import admin
from .models import Subscriptions, Payments, Purchases
admin.site.register(Subscriptions)
admin.site.register(Payments)
admin.site.register(Purchases)
