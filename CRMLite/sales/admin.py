from django.contrib import admin
from .models import Sale, ProductSale

class ProductSaleInline(admin.TabularInline):
    model = ProductSale
    extra = 0
    readonly_fields = ('product', 'quantity', 'sale_price')
    can_delete = False

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'buyer_name', 'company', 'sale_date')
    list_filter = ('company', 'sale_date')
    search_fields = ('buyer_name',)
    inlines = [ProductSaleInline]
    readonly_fields = ('company',)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.company = request.user.company
        super().save_model(request, obj, form, change)