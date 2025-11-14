from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from project.models import Product, Supplier, Vendor, ProductImage, Sale
from django.db.models import Count, Value, F, Sum
from django.db.models.functions import Coalesce, TruncDate
from django.utils import timezone
from datetime import datetime, timedelta
import json

@login_required
def dashboard_view(request):
    # Date filtering
    end_date_str = request.GET.get('end_date')
    start_date_str = request.GET.get('start_date')

    if end_date_str:
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
    else:
        end_date = timezone.now().date()

    if start_date_str:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    else:
        start_date = end_date - timedelta(days=29)

    # Ensure start_date is not after end_date
    if start_date > end_date:
        start_date = end_date - timedelta(days=29)

    # Filter sales by date range
    sales_in_range = Sale.objects.filter(sale_date__date__range=[start_date, end_date])

    # Card stats (some are independent of date)
    product_count = Product.objects.count()
    supplier_count = Supplier.objects.count()
    vendor_count = Vendor.objects.count()
    
    # KPIs (filtered by date)
    sales_aggr = sales_in_range.aggregate(
        total_sales=Sum('total_price'),
        num_sales=Count('id')
    )
    total_sales_value = sales_aggr['total_sales'] or 0
    sales_count = sales_aggr['num_sales'] or 0
    average_sale_value = total_sales_value / sales_count if sales_count > 0 else 0

    # Recent products (independent of date)
    recent_products = Product.objects.order_by('-created_at').prefetch_related('images')[:5]

    # Low stock products (independent of date)
    low_stock_products = Product.objects.filter(stock__lt=5).order_by('stock').prefetch_related('images')

    # Most "active" products (independent of date)
    most_active_products = Product.objects.order_by('-updated_at').prefetch_related('images')[:5]

    # Least "active" products (independent of date)
    least_active_products = Product.objects.order_by('updated_at').prefetch_related('images')[:5]

    # Pie chart data: Products by Supplier (independent of date)
    supplier_data = Product.objects.values(supplier_name=Coalesce('supplier__name', Value('Sem Fornecedor'))) \
        .annotate(count=Count('id')).order_by('-count')
    
    pie_chart_labels = [item['supplier_name'] for item in supplier_data]
    pie_chart_data = [item['count'] for item in supplier_data]

    # Bar chart data: Top 5 Products by Stock (independent of date)
    stock_data = Product.objects.order_by('-stock').prefetch_related('images')[:5]
    bar_chart_labels = [product.name for product in stock_data]
    bar_chart_data = [product.stock for product in stock_data]

    # Line chart data: Sales over time (filtered by date)
    delta = end_date - start_date
    dates = [(start_date + timedelta(days=i)) for i in range(delta.days + 1)]
    
    sales_data_raw = sales_in_range.annotate(date=TruncDate('sale_date')) \
                                   .values('date') \
                                   .annotate(total_sales=Sum('total_price')) \
                                   .order_by('date')
    
    sales_by_date = {sale['date']: sale['total_sales'] for sale in sales_data_raw}
    
    sales_chart_labels = [d.strftime('%d/%m') for d in dates]
    sales_chart_data = [float(sales_by_date.get(d, 0)) for d in dates]

    # Bar chart data: Top 5 Vendors by Sales (filtered by date)
    vendor_sales_data = sales_in_range.values(vendor_name=Coalesce('vendor__name', Value('N/A'))) \
        .annotate(total_sales=Sum('total_price')) \
        .order_by('-total_sales')[:5]

    vendor_sales_labels = [item['vendor_name'] for item in vendor_sales_data]
    vendor_sales_chart_data = [float(item['total_sales']) for item in vendor_sales_data]

    # Doughnut chart data: Top 5 selling products by quantity
    top_products_data = sales_in_range.values('product__name') \
        .annotate(total_quantity=Sum('quantity')) \
        .order_by('-total_quantity')[:5]

    top_products_labels = [item['product__name'] for item in top_products_data]
    top_products_data = [item['total_quantity'] for item in top_products_data]

    context = {
        'product_count': product_count,
        'supplier_count': supplier_count,
        'vendor_count': vendor_count,
        'total_sales_value': total_sales_value,
        'sales_count': sales_count,
        'average_sale_value': average_sale_value,
        'recent_products': recent_products,
        'low_stock_products': low_stock_products,
        'most_active_products': most_active_products,
        'least_active_products': least_active_products,
        'page_title': 'Dashboard',
        'start_date': start_date,
        'end_date': end_date,
        'pie_chart_labels': json.dumps(pie_chart_labels),
        'pie_chart_data': json.dumps(pie_chart_data),
        'bar_chart_labels': json.dumps(bar_chart_labels),
        'bar_chart_data': json.dumps(bar_chart_data),
        'sales_chart_labels': json.dumps(sales_chart_labels),
        'sales_chart_data': json.dumps(sales_chart_data),
        'vendor_sales_labels': json.dumps(vendor_sales_labels),
        'vendor_sales_data': json.dumps(vendor_sales_chart_data),
        'top_products_labels': json.dumps(top_products_labels),
        'top_products_data': json.dumps(top_products_data),
    }
    return render(request, 'dashboard.html', context)


@login_required
def vendor_dashboard_view(request, vendor_id):
    vendor = get_object_or_404(Vendor, pk=vendor_id)

    # Date filtering
    end_date_str = request.GET.get('end_date')
    start_date_str = request.GET.get('start_date')

    if end_date_str:
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
    else:
        end_date = timezone.now().date()

    if start_date_str:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    else:
        start_date = end_date - timedelta(days=29)

    # Ensure start_date is not after end_date
    if start_date > end_date:
        start_date = end_date - timedelta(days=29)

    # Filter sales by date range AND vendor
    sales_in_range = Sale.objects.filter(vendor=vendor, sale_date__date__range=[start_date, end_date])

    # Card stats (some are independent of date)
    product_count = Product.objects.count() # Total products, not vendor specific
    supplier_count = Supplier.objects.count() # Total suppliers, not vendor specific
    vendor_count = Vendor.objects.count() # Total vendors, not vendor specific
    
    # KPIs (filtered by date and vendor)
    sales_aggr = sales_in_range.aggregate(
        total_sales=Sum('total_price'),
        num_sales=Count('id')
    )
    total_sales_value = sales_aggr['total_sales'] or 0
    sales_count = sales_aggr['num_sales'] or 0
    average_sale_value = total_sales_value / sales_count if sales_count > 0 else 0

    # Recent products (independent of date, not vendor specific)
    recent_products = Product.objects.order_by('-created_at').prefetch_related('images')[:5]

    # Low stock products (independent of date, not vendor specific)
    low_stock_products = Product.objects.filter(stock__lt=5).order_by('stock').prefetch_related('images')

    # Most "active" products (independent of date, not vendor specific)
    most_active_products = Product.objects.order_by('-updated_at').prefetch_related('images')[:5]

    # Least "active" products (independent of date, not vendor specific)
    least_active_products = Product.objects.order_by('updated_at').prefetch_related('images')[:5]

    # Pie chart data: Products by Supplier (independent of date, not vendor specific)
    supplier_data = Product.objects.values(supplier_name=Coalesce('supplier__name', Value('Sem Fornecedor'))) \
        .annotate(count=Count('id')).order_by('-count')
    
    pie_chart_labels = [item['supplier_name'] for item in supplier_data]
    pie_chart_data = [item['count'] for item in supplier_data]

    # Bar chart data: Top 5 Products by Stock (independent of date, not vendor specific)
    stock_data = Product.objects.order_by('-stock').prefetch_related('images')[:5]
    bar_chart_labels = [product.name for product in stock_data]
    bar_chart_data = [product.stock for product in stock_data]

    # Line chart data: Sales over time (filtered by date and vendor)
    delta = end_date - start_date
    dates = [(start_date + timedelta(days=i)) for i in range(delta.days + 1)]
    
    sales_data_raw = sales_in_range.annotate(date=TruncDate('sale_date')) \
                                   .values('date') \
                                   .annotate(total_sales=Sum('total_price')) \
                                   .order_by('date')
    
    sales_by_date = {sale['date']: sale['total_sales'] for sale in sales_data_raw}
    
    sales_chart_labels = [d.strftime('%d/%m') for d in dates]
    sales_chart_data = [float(sales_by_date.get(d, 0)) for d in dates]

    # Bar chart data: Top 5 Vendors by Sales (filtered by date, but this chart is for a specific vendor, so it's not "top 5 vendors" but "this vendor's sales")
    # This chart might not make sense in a vendor-specific dashboard, or it should show this vendor's sales vs others.
    # For simplicity, I'll keep it as is, but it will only show data for the current vendor.
    vendor_sales_data = sales_in_range.values(vendor_name=Coalesce('vendor__name', Value('N/A'))) \
        .annotate(total_sales=Sum('total_price')) \
        .order_by('-total_sales')[:5]

    vendor_sales_labels = [item['vendor_name'] for item in vendor_sales_data]
    vendor_sales_chart_data = [float(item['total_sales']) for item in vendor_sales_data]

    # Doughnut chart data: Top 5 selling products by quantity (filtered by date and vendor)
    top_products_data = sales_in_range.values('product__name') \
        .annotate(total_quantity=Sum('quantity')) \
        .order_by('-total_quantity')[:5]

    top_products_labels = [item['product__name'] for item in top_products_data]
    top_products_data = [item['total_quantity'] for item in top_products_data]

    context = {
        'vendor': vendor,
        'product_count': product_count,
        'supplier_count': supplier_count,
        'vendor_count': vendor_count,
        'total_sales_value': total_sales_value,
        'sales_count': sales_count,
        'average_sale_value': average_sale_value,
        'recent_products': recent_products,
        'low_stock_products': low_stock_products,
        'most_active_products': most_active_products,
        'least_active_products': least_active_products,
        'page_title': f'Dashboard do Vendedor: {vendor.name}',
        'start_date': start_date,
        'end_date': end_date,
        'pie_chart_labels': json.dumps(pie_chart_labels),
        'pie_chart_data': json.dumps(pie_chart_data),
        'bar_chart_labels': json.dumps(bar_chart_labels),
        'bar_chart_data': json.dumps(bar_chart_data),
        'sales_chart_labels': json.dumps(sales_chart_labels),
        'sales_chart_data': json.dumps(sales_chart_data),
        'vendor_sales_labels': json.dumps(vendor_sales_labels),
        'vendor_sales_data': json.dumps(vendor_sales_chart_data),
        'top_products_labels': json.dumps(top_products_labels),
        'top_products_data': json.dumps(top_products_data),
    }
    return render(request, 'dashboard/vendor_dashboard.html', context)


@login_required
def supplier_dashboard_view(request, supplier_id):
    supplier = get_object_or_404(Supplier, pk=supplier_id)

    # Date filtering
    end_date_str = request.GET.get('end_date')
    start_date_str = request.GET.get('start_date')

    if end_date_str:
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
    else:
        end_date = timezone.now().date()

    if start_date_str:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    else:
        start_date = end_date - timedelta(days=29)

    # Ensure start_date is not after end_date
    if start_date > end_date:
        start_date = end_date - timedelta(days=29)

    # Filter sales by date range AND supplier's products
    sales_in_range = Sale.objects.filter(product__supplier=supplier, sale_date__date__range=[start_date, end_date])

    # Card stats (some are independent of date)
    product_count = Product.objects.filter(supplier=supplier).count() # Products from this supplier
    total_product_count = Product.objects.count() # Total products in system
    total_supplier_count = Supplier.objects.count() # Total suppliers in system
    total_vendor_count = Vendor.objects.count() # Total vendors in system
    
    # KPIs (filtered by date and supplier)
    sales_aggr = sales_in_range.aggregate(
        total_sales=Sum('total_price'),
        num_sales=Count('id')
    )
    total_sales_value = sales_aggr['total_sales'] or 0
    sales_count = sales_aggr['num_sales'] or 0
    average_sale_value = total_sales_value / sales_count if sales_count > 0 else 0

    # Recent products (independent of date, filtered by supplier)
    recent_products = Product.objects.filter(supplier=supplier).order_by('-created_at').prefetch_related('images')[:5]

    # Low stock products (independent of date, filtered by supplier)
    low_stock_products = Product.objects.filter(supplier=supplier, stock__lt=5).order_by('stock').prefetch_related('images')

    # Most "active" products (independent of date, filtered by supplier)
    most_active_products = Product.objects.filter(supplier=supplier).order_by('-updated_at').prefetch_related('images')[:5]

    # Least "active" products (independent of date, filtered by supplier)
    least_active_products = Product.objects.filter(supplier=supplier).order_by('updated_at').prefetch_related('images')[:5]

    # Pie chart data: Products by Supplier (this chart doesn't make sense for a single supplier dashboard)
    # I'll keep it but it will only show data for the current supplier.
    supplier_data = Product.objects.filter(supplier=supplier).values(supplier_name=Coalesce('supplier__name', Value('Sem Fornecedor'))) \
        .annotate(count=Count('id')).order_by('-count')
    
    pie_chart_labels = [item['supplier_name'] for item in supplier_data]
    pie_chart_data = [item['count'] for item in supplier_data]

    # Bar chart data: Top 5 Products by Stock (filtered by supplier)
    stock_data = Product.objects.filter(supplier=supplier).order_by('-stock').prefetch_related('images')[:5]
    bar_chart_labels = [product.name for product in stock_data]
    bar_chart_data = [product.stock for product in stock_data]

    # Line chart data: Sales over time (filtered by date and supplier)
    delta = end_date - start_date
    dates = [(start_date + timedelta(days=i)) for i in range(delta.days + 1)]
    
    sales_data_raw = sales_in_range.annotate(date=TruncDate('sale_date')) \
                                   .values('date') \
                                   .annotate(total_sales=Sum('total_price')) \
                                   .order_by('date')
    
    sales_by_date = {sale['date']: sale['total_sales'] for sale in sales_data_raw}
    
    sales_chart_labels = [d.strftime('%d/%m') for d in dates]
    sales_chart_data = [float(sales_by_date.get(d, 0)) for d in dates]

    # Bar chart data: Top 5 Vendors by Sales (filtered by date and supplier's products)
    vendor_sales_data = sales_in_range.values(vendor_name=Coalesce('vendor__name', Value('N/A'))) \
        .annotate(total_sales=Sum('total_price')) \
        .order_by('-total_sales')[:5]

    vendor_sales_labels = [item['vendor_name'] for item in vendor_sales_data]
    vendor_sales_chart_data = [float(item['total_sales']) for item in vendor_sales_data]

    # Doughnut chart data: Top 5 selling products by quantity (filtered by date and supplier)
    top_products_data = sales_in_range.values('product__name') \
        .annotate(total_quantity=Sum('quantity')) \
        .order_by('-total_quantity')[:5]

    top_products_labels = [item['product__name'] for item in top_products_data]
    top_products_data = [item['total_quantity'] for item in top_products_data]

    context = {
        'supplier': supplier,
        'product_count': product_count, # Products from this supplier
        'total_product_count': total_product_count,
        'total_supplier_count': total_supplier_count,
        'total_vendor_count': total_vendor_count,
        'total_sales_value': total_sales_value,
        'sales_count': sales_count,
        'average_sale_value': average_sale_value,
        'recent_products': recent_products,
        'low_stock_products': low_stock_products,
        'most_active_products': most_active_products,
        'least_active_products': least_active_products,
        'page_title': f'Dashboard do Fornecedor: {supplier.name}',
        'start_date': start_date,
        'end_date': end_date,
        'pie_chart_labels': json.dumps(pie_chart_labels),
        'pie_chart_data': json.dumps(pie_chart_data),
        'bar_chart_labels': json.dumps(bar_chart_labels),
        'bar_chart_data': json.dumps(bar_chart_data),
        'sales_chart_labels': json.dumps(sales_chart_labels),
        'sales_chart_data': json.dumps(sales_chart_data),
        'vendor_sales_labels': json.dumps(vendor_sales_labels),
        'vendor_sales_data': json.dumps(vendor_sales_chart_data),
        'top_products_labels': json.dumps(top_products_labels),
        'top_products_data': json.dumps(top_products_data),
    }
    return render(request, 'dashboard/supplier_dashboard.html', context)

