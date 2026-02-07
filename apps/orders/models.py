from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from apps.accounts.models import Customer
from apps.items.models import Product
import uuid

# Create your models here.

class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def cart_total(self):
        """Calculate total on the fly to ensure it's always accurate."""
        return sum(item.item_total for item in self.items.all())

    def __str__(self):
        return f"{self.customer.full_name}'s cart"

class CartItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)], default=1)
    
    @property
    def item_total(self):
        return Decimal(self.product.final_price) * self.quantity

    def save(self, *args, **kwargs):
        if self.quantity > self.product.stock:
            raise ValueError(f"Only {self.product.stock} units available.")
        super().save(*args, **kwargs)

# --- ORDER SYSTEM ---

class Order(models.Model):
    STATUS_CHOICES = (
        ("PENDING", "Pending"),
        ("CONFIRMED", "Confirmed"),
        ("SHIPPED", "Shipped"),
        ("CANCELED", "Canceled"),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    order_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} - {self.customer.full_name}"

class OrderItem(models.Model):
    """
    IMPORTANT: This stores the price AT THE TIME OF PURCHASE.
    If the product price changes later, the order history remains accurate.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()

    @property
    def total(self):
        return self.price_at_purchase * self.quantity

# --- PAYMENT SYSTEM ---

class Payment(models.Model):
    PAYMENT_METHODS = (
        ("CH", "Cash"),
        ("DT", "Debit"),
        ("CT", "Credit"),
    )
    
    PAYMENT_STATUS = (
        ("PENDING", "Pending"),
        ("COMPLETED", "Completed"),
        ("FAILED", "Failed"),
        ("REFUNDED", "Refunded"),
    )

    # Use CharField for external transaction IDs (Stripe/PayPal IDs are strings)
    transaction_id = models.CharField(max_length=255, unique=True)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="payment")
    method = models.CharField(max_length=2, choices=PAYMENT_METHODS)
    status = models.CharField(max_length=10, choices=PAYMENT_STATUS, default="PENDING")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Automatically pull total from order if not set
        if not self.amount:
            self.amount = self.order.order_total
        super().save(*args, **kwargs)