from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from .models import Sale, ProductSale
from .serializers import SaleSerializer, SaleCreateSerializer, UpdateSaleSerializer
from products.models import Product
from django.db import transaction

class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return SaleCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return UpdateSaleSerializer
        return SaleSerializer

    def create(self, request, *args, **kwargs):
        serializer = SaleCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            with transaction.atomic():
                sale = Sale.objects.create(
                    buyer_name=serializer.validated_data['buyer_name'],
                    company=request.user.company
                )

                product_ids = [item['product_id'] for item in serializer.validated_data['product_sales']]
                products = Product.objects.filter(
                    id__in=product_ids,
                    storage__company=request.user.company
                )
                product_map = {p.id: p for p in products}

                for item in serializer.validated_data['product_sales']:
                    product = product_map.get(item['product_id'])
                
                    if not product:
                        return Response(
                            {"error": f"Товар с ID {item['product_id']} не найден или не принадлежит вашей компании"},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                
                    if product.quantity < item['quantity']:
                        return Response(
                            {"error": f"Недостаточно товара {product.title}. Доступно: {product.quantity}"},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                
                    ProductSale.objects.create(
                        sale=sale,
                        product=product,
                        quantity=item['quantity'],
                        sale_price=product.sale_price
                    )
                    product.save()

                return Response(
                    SaleSerializer(sale).data,
                    status=status.HTTP_201_CREATED
                )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(SaleSerializer(instance).data)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset().filter(company=request.user.company))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                instance = self.get_object()
                
                product_sales = instance.productsale_set.all()
                for product_sale in product_sales:
                    product = product_sale.product
                    product_sale.delete()
                
                instance.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
                
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )