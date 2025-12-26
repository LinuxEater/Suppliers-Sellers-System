from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Supplier, Vendor, Product # Import the models

@login_required
def home_view(request):
    return render(request, 'home.html')

@login_required
def supplier_list_view(request):
    suppliers = Supplier.objects.all().order_by('-created_at')
    context = {
        'suppliers': suppliers,
        'page_title': 'Administração de Fornecedores'
    }
    return render(request, 'supplier_list.html', context)

@login_required
def vendor_list_view(request):
    vendors = Vendor.objects.all().order_by('-created_at')
    context = {
        'vendors': vendors,
        'page_title': 'Administração de Vendedores'
    }
    return render(request, 'vendor_list.html', context)

@login_required
def product_list_view(request):
    products = Product.objects.all().order_by('-created_at')
    context = {
        'products': products,
        'page_title': 'Lista de Produtos'
    }
    return render(request, 'product/products.html', context)

@login_required
def product_detail_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {
        'product': product,
        'page_title': product.name
    }
    return render(request, 'product/product_detail.html', context)
