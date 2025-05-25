from django.contrib import admin
from django.contrib.auth.admin import UserAdmin 
from .models import CustomUser, UsersProfile

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['email','first_name', 'last_name', 'is_staff', 'is_active',]
    list_filter = ['is_staff', 'is_active']
    fieldsets = (
        (None, {'fields':('email', 'password')}),
        ('Permission', {'fields':('is_staff', 'is_active', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes':('wide',),
            'fields':('email', 'password1', 'password2', 'is_staff', 'is_active')
        }),
    )
    search_fields = ['email']
    ordering = ['email']
admin.site.register(CustomUser, CustomUserAdmin)


admin.site.register(UsersProfile)