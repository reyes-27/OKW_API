from django.contrib import admin
from .models import (
    ProductImage,
    Product,
    )
from .forms import ProductAdminForm
# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm

    fieldsets = (
        (None,
        {'fields':(
            'unit_price',
            'profit',
            'discount',
            'final_price',
            'seller',
            'name',
            'description',
            'stock',
            'rate',
            'visibility',
            'categories',
            'calculate_price',
        ),}
         ),
    )
    readonly_fields = ('final_price', 'rate',)

class ProductImageAdmin(admin.ModelAdmin):
    readonly_fields = ('level',)

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage, ProductImageAdmin)