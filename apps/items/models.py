from django.db import models
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField
from django.core.validators import MaxValueValidator
from django_resized import ResizedImageField
from django.db.models import Sum, F
import uuid
from django.utils.text import slugify
from apps.categories.models import Category
from apps.accounts.models import Customer
from ..constants import VAT_RATE
# Create your models here.
VAT = VAT_RATE
# from .utils import auto_increment_level

import uuid
from django.db import models
from django.core.validators import MaxValueValidator
from django.utils.text import slugify
from ckeditor.fields import RichTextField # Assuming you are using django-ckeditor

class AbstractItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # Changed Float to Decimal to avoid rounding errors in financial math
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    profit = models.IntegerField(
        default=10, 
        blank=True, 
        null=True, 
        help_text="Enter the profit percentage, e.g., 10"
    )
    discount = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(100)], 
        blank=True, 
        default=0
    )
    final_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        blank=True, 
        null=True # Changed to null=True so save() can calculate it
    )

    class Meta:
        abstract = True


class Product(AbstractItem):
    # Added unique=True so URLs remain predictable
    slug = models.SlugField(max_length=150, unique=True, editable=False)
    seller = models.ForeignKey("accounts.Customer", on_delete=models.SET_NULL, null=True, related_name="products")
    name = models.CharField(max_length=70)
    description = RichTextField()
    stock = models.PositiveIntegerField()
    rate = models.PositiveSmallIntegerField(validators=[MaxValueValidator(5)], default=0)
    categories = models.ManyToManyField("categories.Category", blank=True)
    
    VISIBILITY_CHOICES = (
        ("pu", "Public"),
        ("un", "Unlisted"),
        ("pr", "Private"),
    )
    visibility = models.CharField(max_length=2, choices=VISIBILITY_CHOICES, default="pu")
    
    def __str__(self):
        return self.name # Better for Admin visibility than the slug

    def save(self, *args, **kwargs):
        # 1. Validation Logic
        if self.seller and not self.seller.is_seller:
            raise ValueError(f"{self.seller} is not authorized to sell products.")

        # 2. Slug Generation (only on first creation or if name changes)
        if not self.slug:
            self.slug = slugify(self.name)
            # Optional: Handle potential duplicate slugs here

        # 3. Price Calculation Logic
        # Formula: (Price + Profit%) - Discount%
        profit_multiplier = 1 + (self.profit / 100)
        discount_multiplier = 1 - (self.discount / 100)
        self.final_price = (self.unit_price * profit_multiplier) * discount_multiplier

        super().save(*args, **kwargs)

def image_path(instance, filename):
    return f'images/products/{instance.product.slug}/{filename}'
class ProductImage(models.Model):
    image =             ResizedImageField(upload_to=image_path, force_format='png')
    product =           models.ForeignKey(Product, on_delete=models.CASCADE, related_name="image_set")
    level =             models.PositiveSmallIntegerField(default=0,validators=[MaxValueValidator(10)])
    alt_text =          models.CharField(max_length=255, blank=True, null=True)

    @property
    def get_alt_text(self):
        return self.alt_text or self.product.name
    
    def __str__(self):
        return f"{self.product.name} <-> {self.image.name.split("/")[-1]}({self.level})"
    class Meta:
        ordering = ["level"]

    def save(self, *args, **kwargs):
        if not self.pk:
            self.level = ProductImage.objects.filter(product=self.product).count()
            print(self.level)
            
        super().save(*args, **kwargs)

# hola = Product.objects.filter(image_set__gte = 1)