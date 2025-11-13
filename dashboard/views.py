from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from project.models import Product, Supplier, Vendor, ProductImage
from django.db.models import Count, Value, F
from django.db.models.functions import Coalesce
import json

@login_required
def dashboard_view(request):
    # Card stats
    product_count = Product.objects.count()
    supplier_count = Supplier.objects.count()
    vendor_count = Vendor.objects.count()
    
    # Recent products, prefetch images
    recent_products = Product.objects.order_by('-created_at').prefetch_related('images')[:5]

    # Low stock products (less than 5)
    low_stock_products = Product.objects.filter(stock__lt=5).order_by('stock').prefetch_related('images')

    # Most "active" products (proxy for most ordered - based on recent updates)
    # For a real "most ordered" feature, an Order/OrderItem model with quantity would be needed.
    most_active_products = Product.objects.order_by('-updated_at').prefetch_related('images')[:5]

    # Least "active" products (proxy for least ordered - based on least recent updates)
    least_active_products = Product.objects.order_by('updated_at').prefetch_related('images')[:5]

    # Pie chart data: Products by Supplier
    supplier_data = Product.objects.values(supplier_name=Coalesce('supplier__name', Value('Sem Fornecedor'))) \
        .annotate(count=Count('id')).order_by('-count')
    
    pie_chart_labels = [item['supplier_name'] for item in supplier_data]
    pie_chart_data = [item['count'] for item in supplier_data]

    # Bar chart data: Top 5 Products by Stock
    stock_data = Product.objects.order_by('-stock').prefetch_related('images')[:5]
    bar_chart_labels = [product.name for product in stock_data]
    bar_chart_data = [product.stock for product in stock_data]

    context = {
        'product_count': product_count,
        'supplier_count': supplier_count,
        'vendor_count': vendor_count,
        'recent_products': recent_products,
        'low_stock_products': low_stock_products,
        'most_active_products': most_active_products,
        'least_active_products': least_active_products,
        'page_title': 'Dashboard',
        'pie_chart_labels': json.dumps(pie_chart_labels),
        'pie_chart_data': json.dumps(pie_chart_data),
        'bar_chart_labels': json.dumps(bar_chart_labels),
        'bar_chart_data': json.dumps(bar_chart_data),
    }
    return render(request, 'dashboard.html', context)
