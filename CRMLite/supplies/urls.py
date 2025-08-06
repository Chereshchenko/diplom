from django.urls import path, include
from rest_framework.routers import DefaultRouter
from supplies.views import *

router = DefaultRouter()
router.register(r'supplies', SupplyViewSet, basename='supply')

urlpatterns = [
    path('', include(router.urls)),
] 