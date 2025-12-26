from django.urls import path
from .views import home_view, supplier_list_view, vendor_list_view, product_list_view, product_detail_view

urlpatterns = [
    path('', home_view, name='home'),
    path('suppliers/', supplier_list_view, name='supplier_list'),
    path('vendors/', vendor_list_view, name='vendor_list'),
    path('products/', product_list_view, name='product_list'),
    path('products/<uuid:pk>/', product_detail_view, name='product_detail'),
]
