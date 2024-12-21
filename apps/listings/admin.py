from django.contrib import admin
from .models import ProductListing, ListingImage

class ListingImageInline(admin.TabularInline):
    model = ListingImage
    extra = 1

@admin.register(ProductListing)
class ProductListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'seller', 'status', 'created_at')
    list_filter = ('status', 'condition', 'category')
    search_fields = ('title', 'description', 'seller__username')
    inlines = [ListingImageInline]
    date_hierarchy = 'created_at' 