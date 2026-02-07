from django.contrib import admin
from .models import CPUSpecs, GPUSpecs, RAMSpecs, PSUSpecs, CaseSpecs, StorageSpecs, CoolerSpecs, NetworkingSpecs, PC, MotherboardSpecs

# Registering the Product model

# Registering the individual spec models
class CPUSpecsAdmin(admin.ModelAdmin):
    list_display = ('product', 'cores', 'threads', 'base_clock', 'boost_clock', 'tdp')
    search_fields = ('product__name',)

admin.site.register(CPUSpecs, CPUSpecsAdmin)

class GPUSpecsAdmin(admin.ModelAdmin):
    list_display = ('product', 'vram', 'base_clock', "boost_clock", 'memory_clock', 'memory_type','memory_bus', 'bus_interface', 'power_consumption')
    search_fields = ('product__name',)

admin.site.register(GPUSpecs, GPUSpecsAdmin)

class RAMSpecsAdmin(admin.ModelAdmin):
    list_display = ('product', 'capacity', 'type', 'speed')
    search_fields = ('product__name',)

admin.site.register(RAMSpecs, RAMSpecsAdmin)

class PSUSpecsAdmin(admin.ModelAdmin):
    list_display = ('product', 'wattage', 'efficiency')
    search_fields = ('product__name',)

admin.site.register(PSUSpecs, PSUSpecsAdmin)

class CaseSpecsAdmin(admin.ModelAdmin):
    list_display = (
        "product", 
        "form_factor", 
        "motherboard_support", 
        "gpu_clearance", 
        "cpu_cooler_clearance", 
        "psu_clearance", 
        "rgb_lighting"
    )
    list_filter = ("form_factor", "rgb_lighting")
    search_fields = ("product__name", "motherboard_support")
admin.site.register(CaseSpecs, CaseSpecsAdmin)

class StorageSpecsAdmin(admin.ModelAdmin):
    list_display = ('product', 'capacity', 'type', 'read_speed', 'write_speed')
    search_fields = ('product__name',)

admin.site.register(StorageSpecs, StorageSpecsAdmin)

class CoolingSpecsAdmin(admin.ModelAdmin):
    list_display = ('product', 'type', 'fan_size', 'max_rpm')
    search_fields = ('product__name',)

admin.site.register(CoolerSpecs, CoolingSpecsAdmin)

class NetworkingSpecsAdmin(admin.ModelAdmin):
    list_display = ('product', 'ports', 'speed')
    search_fields = ('product__name',)

admin.site.register(NetworkingSpecs, NetworkingSpecsAdmin)

class PCAdmin(admin.ModelAdmin):
    list_display = (
        'product', 
        'motherboard', 
        'cpu', 
        'gpu', 
        'ram', 
        'ram_quantity', 
        'storage', 
        'case', 
        'psu', 
        'cooling', 
        'networking', 
        'aesthetics', 
        'performance', 
        'price',
        )
    list_filter = (
        'motherboard', 
        'cpu', 
        'gpu', 
        'ram', 
        'ram_quantity', 
        'storage', 
        'case', 
        'psu', 
        'cooling', 
        'networking', 
        'aesthetics', 
        'performance', 
        'price'
        )
    search_fields = ('product__name',)
    ordering = ('product',)

    fieldsets = (
        (None, {
            'fields': ('product', 'motherboard', 'cpu', 'gpu', 'ram', 'ram_quantity', 'storage', 'case', 'psu', 'cooling', 'networking','aesthetics', 'performance', 'price',)
        }),
    )

admin.site.register(PC, PCAdmin)

class MotherboardAdmin(admin.ModelAdmin):
    list_display = (
        "socket",
        "form_factor",
        "memory_slots",
        "memory_type",
        "wifi",
    )
    search_fields = (
        "product__name",
    )

admin.site.register(MotherboardSpecs, MotherboardAdmin)