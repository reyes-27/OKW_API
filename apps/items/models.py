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

class AbstractItem(models.Model):
    id =                models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    #Base price of a unit. 
    unit_price =        models.FloatField()
    #If profit is not set by the user, its value will be 10% percent of the unit_price
    profit =           models.IntegerField(default=10, blank=True, null=True, help_text="Enter the profit percentage, for example 10%",)
    discount =          models.PositiveSmallIntegerField(validators=[MaxValueValidator(100)], blank=True, default=0)
    final_price =       models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0)

    # def save(self, *args, **kwargs):
    #     self.final_price = calc_final_price(self.unit_price, self.profit, VAT_RATE)
    #     if self.discount > 0:
    #         self.final_price = round(self.unit_price - self.unit_price * (self.discount / 100), 2)
    #     self.slug = slugify(f"{self.name}_{str(self.id).split("-")[1]}")
    #     super().save(*args, **kwargs)
    class Meta:
        abstract = True


class Product(AbstractItem):
    slug =              models.SlugField(editable=False)
    seller =            models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, related_name="products")
    name =              models.CharField(max_length=70)
    description =       RichTextField()
    stock =             models.PositiveIntegerField()
    rate =              models.PositiveSmallIntegerField(validators=[MaxValueValidator(5)], default=0)
    categories =        models.ManyToManyField(Category, blank=True)
    visibility_choices = (
        ("pu", "Public"),
        ("un", "Unlisted"),
        ("pr", "Private"),
    )
    visibility =        models.CharField(max_length=155, choices=visibility_choices, default="pu")
    
    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        if not self.seller.is_seller:
            raise Exception(f"{self.seller} is not allowed to sell products. Customer object must have the seller property set to True")
        super(Product, self).save(*args, **kwargs)

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