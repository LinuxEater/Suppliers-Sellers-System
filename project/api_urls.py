from django.urls import path
from .api_views import (
    ProductListAPIView, ProductDetailAPIView,
    SupplierListAPIView, SupplierDetailAPIView,
    VendorListAPIView, VendorDetailAPIView,
    SaleListAPIView, SaleDetailAPIView
)

urlpatterns = [
    path('products/', ProductListAPIView.as_view(), name='product-list'),
    path('products/<uuid:pk>/', ProductDetailAPIView.as_view(), name='product-detail'),
    path('suppliers/', SupplierListAPIView.as_view(), name='supplier-list'),
    path('suppliers/<int:pk>/', SupplierDetailAPIView.as_view(), name='supplier-detail'),
    path('vendors/', VendorListAPIView.as_view(), name='vendor-list'),
    path('vendors/<int:pk>/', VendorDetailAPIView.as_view(), name='vendor-detail'),
    path('sales/', SaleListAPIView.as_view(), name='sale-list'),
    path('sales/<int:pk>/', SaleDetailAPIView.as_view(), name='sale-detail'),
]
