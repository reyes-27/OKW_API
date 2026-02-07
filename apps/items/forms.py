from django import forms
from .models import Product
from .utils import calc_final_price
from django.utils.text import slugify
from ..constants import VAT_RATE


class ProductAdminForm(forms.ModelForm):
    calculate_price = forms.BooleanField(required=False)
    class Meta:
        model = Product
        fields = '__all__'
    def save(self, commit=True):
        instance = super().save(commit=False)

        calculate_price = self.cleaned_data.get('calculate_price')
        unit_price = self.cleaned_data.get('unit_price')
        profit = self.cleaned_data.get('profit')
        discount = self.cleaned_data.get('discount')
        name = self.cleaned_data.get('name')

        if calculate_price == True:
            final_price = calc_final_price(unit_price, profit, VAT_RATE)
            if discount > 0:
                final_price = round(unit_price - unit_price * (discount / 100), 2)
            instance.final_price = final_price
        else:
            instance.final_price = unit_price

        if commit:
            instance.save()

        instance.slug = slugify(f"{name}_{instance.id}")
        if commit:
            instance.save()

        return instance