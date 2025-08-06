from django.contrib import admin
from supplies.models import *

@admin.register(Supply)
class SupplyAdmin(admin.ModelAdmin):
    list_display = ('id', 'supplier', 'delivery_date')
    search_fields = ('supplier__title',)
    list_filter = ('supplier', 'delivery_date')

@admin.register(SupplyProduct)
class SupplyProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'supply', 'product', 'quantity', 'purchase_price')
    search_fields = ('product__title', 'supply__id')    