from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Company, Storage

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

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('title', 'inn', 'owner')
    search_fields = ('title', 'inn', 'owner__email')
    raw_id_fields = ('owner',)

@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
    list_display = ('address', 'company')
    search_fields = ('address', 'company__title')
    raw_id_fields = ('company',)