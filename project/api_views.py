from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product, Supplier, Vendor, Sale
from .serializers import ProductSerializer, SupplierSerializer, VendorSerializer, SaleSerializer
from .filters import ProductFilter, SupplierFilter, VendorFilter, SaleFilter

class ProductListAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter

class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class SupplierListAPIView(generics.ListCreateAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = SupplierFilter

class SupplierDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

class VendorListAPIView(generics.ListCreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = VendorFilter

class VendorDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class SaleListAPIView(generics.ListCreateAPIView):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = SaleFilter

class SaleDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
