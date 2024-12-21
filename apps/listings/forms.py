from django import forms
from .models import ProductListing, ListingImage
from apps.categories.models import SubCategory

class ProductListingForm(forms.ModelForm):
    class Meta:
        model = ProductListing
        fields = ['title', 'description', 'price', 'condition', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4}),
            'price': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01'}),
            'condition': forms.Select(attrs={'class': 'form-select'}),
        }