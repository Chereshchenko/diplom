from django.contrib import admin
from suppliers.models import *


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('title', 'inn', 'company')
    search_fields = ('title', 'inn')
    list_filter = ('company',)