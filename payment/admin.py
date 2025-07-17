from django.contrib import admin
from .models import Subscription, Transaction
admin.site.register(Subscription)
admin.site.register(Transaction)