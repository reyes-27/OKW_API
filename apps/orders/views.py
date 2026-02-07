from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import (
    CartSerializer,
    OrderSerializer
)
from apps.items.models import Product
from .models import (
    Order,
    Cart,
    )
from rest_framework import status
from rest_framework.response import Response
from django.db import transaction

from .utils import process_checkout, add_increment_item_to_cart, remove_or_decrement_item, change_quantity

# Create your views here.

class CartDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        """
        Retrieve the current user's cart.
        """
        # Ensure the user has a cart. 
        # Using get_or_create prevents 404s for new users.
        print(request.user)
        cart, created = Cart.objects.get_or_create(customer_id=request.user.customer.id)
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request):
        """
        Optional: Clear the entire cart.
        """
        cart = Cart.objects.filter(customer_id=request.user.customer.id).first()
        if cart:
            cart.items.all().delete()
            return Response({"message": "Cart cleared"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)
    
class CartItemManagerView(APIView):
    def post(self, request, *args, **kwargs):
        cart = Cart.objects.get(customer_id=request.user.customer.id)
        product_id = request.data['product_id']
        quantity = request.data.get('quantity', 1)
        message = add_increment_item_to_cart(cart=cart, product_id=product_id, quantity=quantity)
        if message[0] == 201:
            return Response({"message":message[1]}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message":message[1]}, status=status.HTTP_400_BAD_REQUEST)
    def patch(self, request):
        cart = request.user.customer.cart
        product_id = request.data.get('product_id')
        quantity = request.data['quantity']
        try:
            if quantity is not None:
                msg = change_quantity(cart=cart, product_id=product_id, quantity=quantity)
                return Response({"message": msg})
            msg = remove_or_decrement_item(cart, product_id, force_delete=False)
            return Response({"message": msg})
        except ValueError as e:
            return Response({"error": str(e)}, status=404)

    def delete(self, request, product_id):
        cart = request.user.customer.cart
        # product_id = request.data.get('product_id')
        
        try:
            msg = remove_or_decrement_item(cart, product_id, force_delete=True)
            return Response({"message": msg})
        except ValueError as e:
            return Response({"error": str(e)}, status=404)
        
class CartItemUpdateAPIView(APIView):
    # This handles the "Minus" button
    def patch(self, request):
        cart = request.user.customer.cart
        product_id = request.data.get('product_id')
        
        try:
            message = remove_or_decrement_item(cart, product_id, force_delete=False)
            return Response({'message': message}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)

    # This handles the "Trash Can" (Remove) button
    def delete(self, request):
        cart = request.user.customer.cart
        product_id = request.data.get('product_id') # Or pass in URL
        
        try:
            message = remove_or_decrement_item(cart, product_id, force_delete=True)
            return Response({'message': message}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
    
class OrderListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """View all orders for the logged-in customer."""
        orders = Order.objects.filter(customer__user=request.user).order_by('-created_at')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

class OrderDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        """View details of a specific order."""
        try:
            order = Order.objects.get(pk=pk, customer__user=request.user)
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        except Order.DoesNotExist:
            return Response(
                {"error": "Order not found or access denied."}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
class CheckoutAPIView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            cart = Cart.objects.get(customer=request.user.customer)
        except Cart.DoesNotExist:
            return Response({"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)
        try:
            with transaction.atomic():
                order = process_checkout(cart, payment_method=request.data['payment_method'])
                return Response({
                    "message": "Order created successfully",
                    "order_id": order.id,
                    "total": order.order_total
                }, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({"error": "A server error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

