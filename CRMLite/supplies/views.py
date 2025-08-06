from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from supplies.serializers import *
from products.models import Product
from suppliers.models import Supplier
from users.permissions import IsCompanyEmployee

class SupplyViewSet(viewsets.ModelViewSet):
    serializer_class = SupplySerializer
    permission_classes = [IsAuthenticated, IsCompanyEmployee]
    
    def get_queryset(self):
        return Supply.objects.filter(supplier__company=self.request.user.company)
    
    @action(detail=False, methods=['post'], serializer_class=CreateSupplySerializer)
    def create_supply(self, request):
        serializer = CreateSupplySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        product_ids = [item['id'] for item in serializer.validated_data['products']]
        company_products = Product.objects.filter(
            id__in=product_ids,
            storage__company=request.user.company
        )
        
        if len(company_products) != len(product_ids):
            return Response(
                {"error": "Некоторые товары не принадлежат вашей компании"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        supplier_id = serializer.validated_data['supplier_id']
        if not Supplier.objects.filter(id=supplier_id, company=request.user.company).exists():
            return Response(
                {"error": "Поставщик не принадлежит вашей компании"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        supply = Supply.objects.create(
            supplier_id=serializer.validated_data['supplier_id'],
            delivery_date=serializer.validated_data.get('delivery_date')
        )
        
        for item in serializer.validated_data['products']:
            product = Product.objects.get(id=item['id'])
            SupplyProduct.objects.create(
                supply=supply,
                product=product,
                quantity=item['quantity'],
                purchase_price=item.get('purchase_price', product.purchase_price)
            )
        
        return Response(SupplySerializer(supply).data, status=status.HTTP_201_CREATED)