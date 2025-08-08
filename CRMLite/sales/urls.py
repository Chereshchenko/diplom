from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SaleViewSet

router = DefaultRouter()
router.register(r'sales', SaleViewSet, basename='sale')

urlpatterns = [
    path('sales/create_sale/', SaleViewSet.as_view({'post': 'create'})), 
    path('sales/list/', SaleViewSet.as_view({'get': 'list'})),
    path('sales/<int:pk>/update/', SaleViewSet.as_view({'patch': 'update'}), name='update-sale'),
    path('sales/<int:pk>/delete/', SaleViewSet.as_view({'delete': 'destroy'}), name='delete-sale'),
] 