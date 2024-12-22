from django import forms
from .models import ProductListing, ListingImage, Comment
from apps.categories.models import SubCategory

class ProductListingForm(forms.ModelForm):
    class Meta:
        model = ProductListing
        fields = ['title', 'description', 'price', 'condition', 'category', 'status', 'is_available']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make sure all required fields are properly marked
        self.fields['title'].required = True
        self.fields['description'].required = True
        self.fields['price'].required = True
        self.fields['condition'].required = True
        self.fields['category'].required = True
        
    def clean(self):
        cleaned_data = super().clean()
        print(f"\nForm Cleaning Debug:")
        print(f"Cleaned data: {cleaned_data}")
        return cleaned_data

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price and price < 0:
            raise forms.ValidationError("Price cannot be negative")
        return price

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 3,
                'class': 'comment-input',
                'placeholder': 'Write your comment...',
                'maxlength': 1000
            })
        }

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content.strip()) < 1:
            raise forms.ValidationError("Comment cannot be empty.")
        return content