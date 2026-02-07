from django.urls import path
from .views import (
    CartDetailAPIView,
    CartItemManagerView,
    CheckoutAPIView, 
    OrderListAPIView, 
    OrderDetailAPIView
)
urlpatterns = [
    # The Cart itself
    path('cart/', CartDetailAPIView.as_view(), name='cart-detail'),
    
    # Items inside the cart
    path('cart/items/', CartItemManagerView.as_view(), name='cart-items'),
    path('cart/items/<uuid:product_id>/', CartItemManagerView.as_view(), name='cart-items'),

    
    # Process the cart
    path('cart/checkout/', CheckoutAPIView.as_view(), name='checkout'),
    
    # Finalized Orders
    path('orders/', OrderListAPIView.as_view(), name='order-list'),
    path('orders/<uuid:pk>/', OrderDetailAPIView.as_view(), name='order-detail'),
]