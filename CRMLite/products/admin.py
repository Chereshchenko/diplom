from django.contrib import admin
from products.models import *


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'purchase_price', 'sale_price', 'quantity', 'storage')
    search_fields = ('name',)
    list_filter = ('storage',)