import django_filters
from .models import Product, Supplier, Vendor, Sale

class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    product_code = django_filters.CharFilter(lookup_expr='icontains')
    supplier = django_filters.NumberFilter(field_name='supplier__id')
    min_stock = django_filters.NumberFilter(field_name='stock', lookup_expr='gte')
    max_stock = django_filters.NumberFilter(field_name='stock', lookup_expr='lte')
    is_active = django_filters.BooleanFilter()

    class Meta:
        model = Product
        fields = ['name', 'product_code', 'supplier', 'min_stock', 'max_stock', 'is_active']

class SupplierFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    contact_email = django_filters.CharFilter(lookup_expr='icontains')
    contact_phone = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Supplier
        fields = ['name', 'contact_email', 'contact_phone']

class VendorFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    phone = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Vendor
        fields = ['name', 'phone']

class SaleFilter(django_filters.FilterSet):
    product = django_filters.NumberFilter(field_name='product__id')
    vendor = django_filters.NumberFilter(field_name='vendor__id')
    platform = django_filters.CharFilter(lookup_expr='exact')
    min_total_price = django_filters.NumberFilter(field_name='total_price', lookup_expr='gte')
    max_total_price = django_filters.NumberFilter(field_name='total_price', lookup_expr='lte')
    start_date = django_filters.DateFilter(field_name='sale_date', lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name='sale_date', lookup_expr='lte')

    class Meta:
        model = Sale
        fields = ['product', 'vendor', 'platform', 'min_total_price', 'max_total_price', 'start_date', 'end_date']
