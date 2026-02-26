from django import forms
from .models import Product
from django.utils.text import slugify

class ProductAdminForm(forms.ModelForm):
    # This remains as a UI toggle
    calculate_price = forms.BooleanField(required=False, initial=True)

    class Meta:
        model = Product
        fields = '__all__'

    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # If 'calculate_price' is UNCHECKED, we skip the model's auto-calc
        # by manually setting final_price to unit_price here.
        if not self.cleaned_data.get('calculate_price'):
            instance.final_price = instance.unit_price
        
        # We don't need to manually slugify here anymore because the 
        # model's save() method (which we fixed earlier) handles it.
        
        if commit:
            instance.save()
            # If you specifically want the ID in the slug (name_uuid):
            if not instance.slug:
                instance.slug = slugify(f"{instance.name}-{instance.id}")
                instance.save()
                
        return instance