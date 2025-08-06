from django.urls import path, include
from rest_framework.routers import DefaultRouter
from companies.views import *

router = DefaultRouter()
router.register(r'companies', CompanyViewSet, basename='company')
router.register(r'storages', StorageViewSet, basename='storage')

urlpatterns = [
    path('', include(router.urls)),
]