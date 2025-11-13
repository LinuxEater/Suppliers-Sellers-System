from django.urls import path
from .views import home_view, supplier_list_view, vendor_list_view

urlpatterns = [
    path('', home_view, name='home'),
    path('suppliers/', supplier_list_view, name='supplier_list'),
    path('vendors/', vendor_list_view, name='vendor_list'),
]
