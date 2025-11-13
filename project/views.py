from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Supplier, Vendor # Import the models

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
