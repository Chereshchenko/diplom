from django.urls import path, include

urlpatterns = [
    path('auth/', include('users.urls')),
    path('companies/', include('companies.urls')),
    path('suppliers/', include('suppliers.urls')),
    path('products/', include('products.urls')),
    path('sales/', include('sales.urls')),
    path('supplies/', include('supplies.urls')),
]