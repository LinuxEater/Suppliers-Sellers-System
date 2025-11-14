from django.urls import path
from .views import dashboard_view, vendor_dashboard_view, supplier_dashboard_view

urlpatterns = [
    path('', dashboard_view, name='dashboard'),
    path('vendor/<int:vendor_id>/', vendor_dashboard_view, name='vendor_dashboard'),
    path('supplier/<int:supplier_id>/', supplier_dashboard_view, name='supplier_dashboard'),
]
