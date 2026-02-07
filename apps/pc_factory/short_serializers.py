from rest_framework import serializers
from .models import(
    MotherboardSpecs,
    CPUSpecs,
    GPUSpecs,
    RAMSpecs,
    PSUSpecs,
    CaseSpecs,
    StorageSpecs,
    CoolerSpecs,
    NetworkingSpecs,
)

class ShortMotherboardSpecsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MotherboardSpecs
        fields = ['socket', 'form_factor', 'chipset', 'max_memory', 'memory_type']

class ShortCPUSpecsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CPUSpecs
        fields = ['cores', 'threads', 'base_clock', 'boost_clock', 'tdp']

class ShortGPUSpecsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GPUSpecs
        fields = ['vram', 'boost_clock', 'memory_type', 'power_consumption']

class ShortRAMSpecsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RAMSpecs
        fields = ['capacity', 'type', 'speed', 'rgb']

class ShortPSUSpecsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PSUSpecs
        fields = ['wattage', 'efficiency']

class ShortCaseSpecsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseSpecs
        fields = ['form_factor', 'gpu_clearance', 'psu_clearance', 'rgb_lighting']

class ShortStorageSpecsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorageSpecs
        fields = ['capacity', 'type', 'read_speed', 'write_speed']

class ShortCoolerSpecsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoolerSpecs
        fields = ['type', 'fan_size', 'max_rpm', 'tdp_rating', 'rgb_lighting']

class ShortNetworkingSpecsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkingSpecs
        fields = ['ports', 'speed']