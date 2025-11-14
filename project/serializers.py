from rest_framework import serializers
from .models import Product, Supplier, Vendor, Sale, ProductImage, PlatformFeeConfig, StockHistory

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    supplier = SupplierSerializer(read_only=True) # Nested serializer for supplier details

    class Meta:
        model = Product
        fields = '__all__'

class SaleSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True) # Nested serializer for product details
    vendor = VendorSerializer(read_only=True) # Nested serializer for vendor details

    class Meta:
        model = Sale
        fields = '__all__'

class PlatformFeeConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlatformFeeConfig
        fields = '__all__'

class StockHistorySerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True) # Nested serializer for product details

    class Meta:
        model = StockHistory
        fields = '__all__'
