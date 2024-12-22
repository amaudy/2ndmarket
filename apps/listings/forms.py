from django import forms
from .models import ProductListing, ListingImage
from apps.categories.models import SubCategory

class ProductListingForm(forms.ModelForm):
    class Meta:
        model = ProductListing
        fields = ['title', 'description', 'price', 'condition', 'category', 'status', 'is_available']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add any form field customization here
        
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price and price < 0:
            raise forms.ValidationError("Price cannot be negative")
        return price