from import_export import resources
from .models import Product, Supplier

class ProductResource(resources.ModelResource):
    class Meta:
        model = Product
        fields = (
            'id',
            'product_code',
            'name',
            'description',
            'supplier__name', # Export supplier name instead of ID
            'cost_price',
            'recommended_price',
            'negotiation_margin',
            'stock',
            'is_active',
            'created_at',
            'updated_at',
        )
        export_order = fields # Maintain the order of fields during export

    def before_import_row(self, row, **kwargs):
        # Handle supplier by name
        supplier_name = row.get('supplier__name')
        if supplier_name:
            supplier, created = Supplier.objects.get_or_create(name=supplier_name)
            row['supplier'] = supplier.pk # Set supplier to its primary key for import
        else:
            row['supplier'] = None # Handle cases where supplier name is not provided
