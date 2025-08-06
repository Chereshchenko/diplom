from django.contrib import admin
from companies.models import *

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

