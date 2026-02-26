from rest_framework import serializers
from .models import (
    CartItem,
    Order,
    Cart,
    OrderItem
)
from apps.ecommerce.serializers import ProductSerializer
from apps.accounts.serializers import CustomerSerializer



class CartItemSerializer(serializers.ModelSerializer):
    product__name = serializers.ReadOnlyField(source='product.name')
    product__unit_price = serializers.ReadOnlyField(source='product.final_price')
    product__stock = serializers.ReadOnlyField(source='product.stock')
    product__slug = serializers.ReadOnlyField(source='product.slug')
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, source='item_total', read_only=True)
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        images = getattr(obj.product, 'primary_images', [])
        image_obj = images[0] if images else None
        if image_obj and image_obj.image:
            request = self.context.get('request')
            if request is not None:
                return request.build_absolute_uri(image_obj.image.url)
            return image_obj.image.url
        return None

        
    class Meta:
            model = CartItem
            fields = [
                'id', 
                'product__name',
                'product__stock',
                'product__slug', 
                'product__unit_price', 
                'quantity', 
                'subtotal', 
                'image', 
                ]
            

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, source='cart_total', read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price', 'created_at']

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'price_at_purchase', 'quantity', 'total']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    payment_status = serializers.CharField(source='payment.status', read_only=True)
    payment_method = serializers.CharField(source='payment.get_method_display', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'status', 'order_total', 'items', 
            'payment_status', 'payment_method', 'created_at'
        ]