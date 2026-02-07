from rest_framework.serializers import (
    HyperlinkedModelSerializer,
    HyperlinkedIdentityField,
    ModelSerializer,
    SerializerMethodField,
    )
from apps.items.models import (
    Product,
    ProductImage,
    )

from apps.categories.serializers import CategorySerializer
from apps.accounts.serializers import ShortCustomerSerializer
from apps.pc_factory import serializers as SpecSerializers

SPECS_SERIALIZERS_LIST ={
        'CPU': (lambda obj:SpecSerializers.CPUSpecsSerializer(getattr(obj, 'cpu_specs', None)).data),
        'GPU': (lambda obj:SpecSerializers.GPUSpecsSerializer(getattr(obj, 'gpu_specs', None)).data),
        'PSU': (lambda obj:SpecSerializers.PSUSpecsSerializer(getattr(obj, 'psu_specs', None)).data),
        'RAM': (lambda obj:SpecSerializers.RAMSpecsSerializer(getattr(obj, 'ram_specs', None)).data),
        'Cooler': (lambda obj:SpecSerializers.CoolerSpecsSerializer(getattr(obj, 'cooler_specs', None)).data),
        'Case': (lambda obj:SpecSerializers.CaseSpecsSerializer(getattr(obj, 'case_specs', None)).data),
        'Storage': (lambda obj:SpecSerializers.StorageSpecsSerializer(getattr(obj, 'storage_specs', None)).data),
        'Motherboard': (lambda obj:SpecSerializers.MotherboardSpecsSerializer(getattr(obj, 'motherboard_specs', None)).data),
        'Networking': (lambda obj:SpecSerializers.NetworkingSpecsSerializer(getattr(obj, 'networking_specs', None)).data),
        'PC': (lambda obj:SpecSerializers.PCSpecsSerializer(getattr(obj, 'PC_specs', None)).data),
}
class ProductImageSerializer(ModelSerializer):
    class Meta:
        model = ProductImage
        fields = [
            "image",
            "level",
            "alt_text",
        ]

class ProductSerializer(HyperlinkedModelSerializer):
    url = HyperlinkedIdentityField(
        view_name = "product-detail",
        lookup_field = "slug",
        lookup_url_kwarg = "slug",
        )
    image_set = ProductImageSerializer(many=True, read_only=True)
    seller = ShortCustomerSerializer(read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    specs = SerializerMethodField()


    def get_specs(self, obj):
        category = obj.categories.first()
        serializer_fn = SPECS_SERIALIZERS_LIST.get(category.name)
        return serializer_fn(obj=obj) if serializer_fn else None

    class Meta:
        model = Product
        fields = "__all__"

class ShortProductSerializer(HyperlinkedModelSerializer):
    url = HyperlinkedIdentityField(
        view_name = "product-detail",
        lookup_field = "slug",
        lookup_url_kwarg = "slug",
        )
    image_set = ProductImageSerializer(many=True, read_only=True)
    seller = ShortCustomerSerializer(read_only=True)
    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = "__all__"
