from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from products.serializers import *
from users.permissions import IsCompanyEmployee

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsCompanyEmployee]
    
    def get_queryset(self):
        return Product.objects.filter(storage__company=self.request.user.company)
    
    def perform_create(self, serializer):
        storage = serializer.validated_data['storage']
        if storage.company != self.request.user.company:
            raise serializers.ValidationError("Вы можете добавлять товары только на свои склады")
        serializer.save(quantity=0)