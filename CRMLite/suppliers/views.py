from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from suppliers.serializers import *
from users.permissions import IsCompanyEmployee
        
class SupplierViewSet(viewsets.ModelViewSet):
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated, IsCompanyEmployee]
    
    def get_queryset(self):
        return Supplier.objects.filter(company=self.request.user.company)
    def perform_create(self, serializer):
        serializer.save(company=self.request.user.company)