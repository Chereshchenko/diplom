from django.urls import path, include
from rest_framework.routers import DefaultRouter
from suppliers.views import *

router = DefaultRouter()
router.register(r'suppliers', SupplierViewSet, basename='supplier')

urlpatterns = [
    path('', include(router.urls)),
]