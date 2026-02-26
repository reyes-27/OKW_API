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
    product_name = serializers.ReadOnlyField(source='product.name')
    unit_price = serializers.ReadOnlyField(source='product.final_price')
    # Use the @property we created in the model
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, source='item_total', read_only=True)
    image = serializers.SerializerMethodField()
    stock = serializers.SerializerMethodField()
    def get_image(self, obj):
        image_obj = obj.product.image_set.filter(level=0).first()
        if image_obj and image_obj.image:
            request = self.context.get('request')
            if request is not None:
                return request.build_absolute_uri(image_obj.image.url)
            return image_obj.image.url
        return None
    def get_stock(self, obj):
        return obj.product.stock
        
    class Meta:
            model = CartItem
            fields = ['id', 'product', 'product_name', 'quantity', 'unit_price', 'subtotal', 'image', 'stock']
            

    

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    # Use the @property from the Cart model
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, source='cart_total', read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price', 'created_at']

# class ShortCartSerializer()

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    # Use the property for total (quantity * price_at_purchase)
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