from rest_framework import serializers
from .models import Sale, ProductSale
from products.models import Product

class ProductSaleCreateSerializer(serializers.Serializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    quantity = serializers.IntegerField(min_value=1)


class ProductSaleInputSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

class SaleCreateSerializer(serializers.Serializer):
    buyer_name = serializers.CharField(max_length=255)
    product_sales = serializers.ListField(
        child=ProductSaleInputSerializer(),
    )

class ProductSaleOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSale
        fields = ['product', 'quantity', 'sale_price']
        read_only_fields = fields
    
    
class ProductSaleItemSerializer(serializers.Serializer):
    product = serializers.IntegerField() 
    quantity = serializers.IntegerField(min_value=1)

    def validate_product(self, value):
        try:
            product = Product.objects.get(id=value)
            if product.storage.company != self.context['request'].user.company:
                raise serializers.ValidationError("Товар не принадлежит вашей компании")
            return value
        except Product.DoesNotExist:
            raise serializers.ValidationError("Товар не найден")    

class ProductSaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSale
        fields = ['product', 'quantity', 'sale_price']
        read_only_fields = fields 

class SaleSerializer(serializers.ModelSerializer):
    product_sales = ProductSaleSerializer(many=True, read_only=True, source='productsale_set')
    
    class Meta:
        model = Sale
        fields = ['id', 'buyer_name', 'sale_date', 'company', 'product_sales']
        read_only_fields = ['id', 'sale_date', 'company']

class UpdateSaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = ['buyer_name', 'sale_date']
        extra_kwargs = {
            'buyer_name': {'required': False},
            'sale_date': {'required': False}
        }
        