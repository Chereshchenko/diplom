from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import *

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'is_company_owner', 'company')
    search_fields = ('email',)
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_company_owner', 'company')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
