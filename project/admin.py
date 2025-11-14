from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from django.utils.html import format_html
from .models import Supplier, Vendor, Product, ProductImage, PlatformFeeConfig, Sale, StockHistory
from .resources import ProductResource


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_email', 'contact_phone', 'view_dashboard_link', 'created_at')
    search_fields = ('name', 'contact_email', 'contact_phone')
    list_filter = ('created_at',)
    ordering = ('-created_at',)

    def view_dashboard_link(self, obj):
        from django.urls import reverse
        link = reverse('supplier_dashboard', args=[obj.pk])
        return format_html('<a href="{}">Ver Dashboard</a>', link)
    view_dashboard_link.short_description = 'Dashboard'
    view_dashboard_link.allow_tags = True


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('vendor_profile_thumbnail', 'name', 'phone', 'view_dashboard_link', 'created_at') # Added thumbnail and dashboard link
    search_fields = ('name', 'phone')
    list_filter = ('created_at',)
    fieldsets = ( # Added fieldsets to include profile_image
        (None, {
            'fields': ('user', 'name', 'phone', 'profile_image')
        }),
    )

    def vendor_profile_thumbnail(self, obj):
        if obj.profile_image:
            return format_html('<img src="{}" width="50" style="border-radius:50%;" />', obj.profile_image.url)
        return '(Sem Imagem)'
    vendor_profile_thumbnail.short_description = 'Imagem de Perfil'

    def view_dashboard_link(self, obj):
        from django.urls import reverse
        link = reverse('vendor_dashboard', args=[obj.pk])
        return format_html('<a href="{}">Ver Dashboard</a>', link)
    view_dashboard_link.short_description = 'Dashboard'
    view_dashboard_link.allow_tags = True


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0
    max_num = 5  # limita 5 imagens por produto
    fields = ('image', 'alt_text', 'position', 'preview')
    readonly_fields = ('preview',)

    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="80" style="border-radius:8px;" />', obj.image.url)
        return '(sem imagem)'
    preview.short_description = 'Pré-visualização'


class StockHistoryInline(admin.TabularInline):
    model = StockHistory
    extra = 0
    readonly_fields = ('change', 'reason', 'timestamp')
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin): # Inherit from ImportExportModelAdmin
    resource_class = ProductResource # Add resource_class
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
    inlines = [ProductImageInline, StockHistoryInline]

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
            return format_html('<img src="{}" width="50" style="border-radius:8px;" />', obj.images.first().image.url)
        return '(Sem Imagem)'
    product_image_thumbnail.short_description = 'Imagem'


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


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('product', 'vendor', 'quantity', 'total_price', 'platform', 'sale_date')
    list_filter = ('platform', 'sale_date', 'vendor')
    search_fields = ('product__name', 'vendor__name')
    date_hierarchy = 'sale_date'


@admin.register(StockHistory)
class StockHistoryAdmin(admin.ModelAdmin):
    list_display = ('product', 'change', 'reason', 'timestamp')
    list_filter = ('reason', 'timestamp')
    search_fields = ('product__name',)
    date_hierarchy = 'timestamp'

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
