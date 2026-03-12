from django import forms
from .models import Product
from django.utils.text import slugify
from decimal import Decimal

class ProductAdminForm(forms.ModelForm):
    calculate_price = forms.BooleanField(required=False, initial=False)
    class Meta:
        model = Product
        fields = '__all__'
    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.cleaned_data.get('calculate_price'):
            profit_multiplier = Decimal('1') + (Decimal(str(instance.profit)) / Decimal('100'))
            discount_multiplier = Decimal('1') - (Decimal(str(instance.discount)) / Decimal('100'))
            instance.final_price = (instance.unit_price * profit_multiplier) * discount_multiplier
        if commit:
            instance.save()
            if not instance.slug:
                instance.slug = slugify(f"{instance.name}-{instance.id}")
                instance.save()
                
        return instance