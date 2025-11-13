from django.contrib import admin
from .models import Supplier, Vendor, Product, ProductImage, PlatformFeeConfig


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_email', 'contact_phone', 'created_at')
    search_fields = ('name', 'contact_email', 'contact_phone')
    list_filter = ('created_at',)
    ordering = ('-created_at',)


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('vendor_profile_thumbnail', 'name', 'phone', 'created_at') # Added thumbnail
    search_fields = ('name', 'phone')
    list_filter = ('created_at',)
    fieldsets = ( # Added fieldsets to include profile_image
        (None, {
            'fields': ('user', 'name', 'phone', 'profile_image')
        }),
    )

    def vendor_profile_thumbnail(self, obj):
        if obj.profile_image:
            return f'<img src="{obj.profile_image.url}" width="50" style="border-radius:50%;" />'
        return '(Sem Imagem)'
    vendor_profile_thumbnail.short_description = 'Imagem de Perfil'
    vendor_profile_thumbnail.allow_tags = True


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0
    max_num = 5  # limita 5 imagens por produto
    fields = ('image', 'alt_text', 'position', 'preview')
    readonly_fields = ('preview',)

    def preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="80" style="border-radius:8px;" />'
        return '(sem imagem)'
    preview.allow_tags = True
    preview.short_description = 'Pré-visualização'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'product_image_thumbnail', # Added for image display
        'product_code',
        'name',
        'supplier',
        'cost_price',
        'recommended_price',
        'vf_fisica',
        'vf_shopee',
        'stock',
        'is_active',
        'created_at',
    )
    list_filter = ('is_active', 'supplier', 'created_at')
    search_fields = ('product_code', 'name', 'supplier__name')
    readonly_fields = ('created_at', 'updated_at', 'vf_fisica', 'vf_shopee', 'min_price_allowed')
    inlines = [ProductImageInline]

    fieldsets = (
        ('Informações do Produto', {
            'fields': ('product_code', 'name', 'description', 'supplier', 'stock', 'is_active')
        }),
        ('Preços e Margens', {
            'fields': ('cost_price', 'recommended_price', 'negotiation_margin', 'vf_fisica', 'vf_shopee', 'min_price_allowed')
        }),
        ('Mídia', {
            'fields': ('video_file',)
        }),
        ('Datas', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    def product_image_thumbnail(self, obj):
        if obj.images.first():
            return f'<img src="{obj.images.first().image.url}" width="50" style="border-radius:8px;" />'
        return '(Sem Imagem)'
    product_image_thumbnail.short_description = 'Imagem'
    product_image_thumbnail.allow_tags = True


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'position', 'image', 'created_at')
    list_filter = ('product',)
    search_fields = ('product__name', 'product__product_code')
    ordering = ('product', 'position')


@admin.register(PlatformFeeConfig)
class PlatformFeeConfigAdmin(admin.ModelAdmin):
    list_display = (
        'cost_fixed',
        'physical_margin',
        'shopee_commission',
        'free_shipping_fee',
        'fixed_fee',
        'highlight_active',
        'highlight_fee',
    )
    fieldsets = (
        ('Configurações Gerais', {
            'fields': (
                'cost_fixed',
                'physical_margin',
                'shopee_commission',
                'free_shipping_fee',
                'fixed_fee',
                'highlight_active',
                'highlight_fee',
            )
        }),
    )

    def has_add_permission(self, request):
        # permite apenas uma configuração global
        return not PlatformFeeConfig.objects.exists()
