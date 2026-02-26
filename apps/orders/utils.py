from .models import Order, OrderItem, Payment, CartItem
from django.db import transaction
from ..items.models import Product
def process_checkout(cart, payment_method):
    """
    This function will take 2 arguments, current user's cart(Cart to be converted to order)
    and a Payment linked to the order to freeze prices to ensure consistency
    this function will run atomically, to make sure this opration is completely successful or nothing happens
    """
    valid_methods = [choice[0] for choice in Payment.PAYMENT_METHODS]
    if payment_method not in valid_methods:
        raise ValueError(f"Invalid payment method: '{payment_method}'.")
    with transaction.atomic():
        items = cart.items.all()
        if not items.exists():
            raise ValueError('Cannot checkout with an empty cart.')
        order = Order.objects.create(
            customer=cart.customer,
            order_total=cart.cart_total,
            status="CONFIRMED"
        )
        for item in items:
            if item.quantity > item.product.quantity:
                raise ValueError(f"Not enough stock for {item.product.name}")
            OrderItem.objects.create(
                order=order,
                product=item.product,
                price_at_purchase=item.product.final_price,
                quantity=item.quantity,
            )

            product=item.product
            product.quantity-=item.quantity
            product.save()
        Payment.objects.create(
            order=order,
            method=payment_method,
            amount=order.order_total,
            transaction_id=f"TXN-{order.id.hex[:10].upper()}",
            status="PENDING"
        )
        items.delete()
        return order
    
def add_increment_item_to_cart(cart, product_slug, quantity):
    product = Product.objects.get(slug=product_slug)
    item, created = CartItem.objects.get_or_create(
        product=product, 
        cart=cart, 
        defaults={'quantity': quantity}
    )
    if not created:
        item.quantity += quantity
    try:
        item.save()
        message = [201, "Item added to cart"]
    except ValueError as e:
        message = [400, f'error: {e}']
    return message

def remove_or_decrement_item(cart, product_id, force_delete=False):
    try:
        item = CartItem.objects.get(product_id=product_id, cart=cart)
        
        if force_delete or item.quantity <= 1:
            item.delete()
            return "Item removed from cart"
        
        item.quantity -= 1
        item.save()
        return "Item quantity decremented"
        
    except CartItem.DoesNotExist:
        raise ValueError("Item not found in cart")
    
def change_quantity(cart, product_id, quantity):
    try:
        quantity = int(quantity)
        item = CartItem.objects.get(product_id=product_id, cart=cart)

        if quantity > 0:
            item.quantity = quantity
            item.save()
            return 'Quantity changed successfully'
        
        # If they enter 0 or less, just remove it. Cleaner UX!
        item.delete()
        return 'Item removed from cart'

    except (CartItem.DoesNotExist, ValueError, TypeError):
        # Catching TypeError/ValueError in case int() fails
        raise ValueError("Invalid request: Check product ID or quantity format")

