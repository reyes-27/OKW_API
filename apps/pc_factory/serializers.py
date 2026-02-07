from rest_framework.serializers import ModelSerializer
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
    PC,
)

from .short_serializers import (
    ShortMotherboardSpecsSerializer,
    ShortCPUSpecsSerializer,
    ShortGPUSpecsSerializer,
    ShortRAMSpecsSerializer,
    ShortPSUSpecsSerializer,
    ShortCaseSpecsSerializer,
    ShortStorageSpecsSerializer,
    ShortCoolerSpecsSerializer,
    ShortNetworkingSpecsSerializer,
)


class CPUSpecsSerializer(ModelSerializer):
    class Meta:
        model = CPUSpecs
        exclude = ["product"]

class GPUSpecsSerializer(ModelSerializer):
    class Meta:
        model = GPUSpecs
        exclude = ["product"]

class RAMSpecsSerializer(ModelSerializer):
    class Meta:
        model = RAMSpecs
        exclude = ["product"]

class PSUSpecsSerializer(ModelSerializer):
    class Meta:
        model = PSUSpecs
        exclude = ["product"]

class CaseSpecsSerializer(ModelSerializer):
    class Meta:
        model = CaseSpecs
        exclude = ["product"]

class StorageSpecsSerializer(ModelSerializer):
    class Meta:
        model = StorageSpecs
        exclude = ["product"]

class CoolerSpecsSerializer(ModelSerializer):
    class Meta:
        model = CoolerSpecs
        exclude = ["product"]

class NetworkingSpecsSerializer(ModelSerializer):
    class Meta:
        model = NetworkingSpecs
        exclude = ["product"]

class MotherboardSpecsSerializer(ModelSerializer):
    class Meta:
        model = MotherboardSpecs
        exclude = ["product"]

class PCSpecsSerializer(ModelSerializer):
    motherboard = ShortMotherboardSpecsSerializer(read_only=True)
    cpu = ShortCPUSpecsSerializer(read_only=True)
    gpu = ShortGPUSpecsSerializer(read_only=True)
    ram = ShortRAMSpecsSerializer(read_only=True)
    psu = ShortPSUSpecsSerializer(read_only=True)
    case = ShortCaseSpecsSerializer(read_only=True)
    storage = ShortStorageSpecsSerializer(read_only=True)
    cooling = ShortCoolerSpecsSerializer(read_only=True)
    networking = ShortNetworkingSpecsSerializer(read_only=True)

    class Meta:
        model = PC
        exclude = ["product"]
 