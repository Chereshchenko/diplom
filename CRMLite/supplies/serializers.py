from rest_framework import serializers
from supplies.models import SupplyProduct, Supply
from products.serializers import ProductSerializer

class SupplyProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    
    class Meta:
        model = SupplyProduct
        fields = '__all__'

class SupplySerializer(serializers.ModelSerializer):
    supply_products = SupplyProductSerializer(many=True, read_only=True)
    
    class Meta:
        model = Supply
        fields = '__all__'

class SupplyProductItemSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)
    purchase_price = serializers.DecimalField(
        max_digits=10, 
        decimal_places=2,
        required=False 
    )

class CreateSupplySerializer(serializers.Serializer):
    supplier_id = serializers.IntegerField()
    delivery_date = serializers.DateField(required=False)
    products = serializers.ListField(
        child=SupplyProductItemSerializer()
    )