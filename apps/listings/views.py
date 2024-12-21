from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.db import transaction
from django.views.generic import ListView, DetailView
from django.core.exceptions import ValidationError
from .models import ProductListing, ListingImage
from .forms import ProductListingForm
from django.http import JsonResponse
from django.views.generic.edit import DeleteView

class CreateListingView(LoginRequiredMixin, CreateView):
    model = ProductListing
    form_class = ProductListingForm
    template_name = 'listings/create_listing.html'
    success_url = reverse_lazy('listings:my-listings')

    def form_valid(self, form):
        form.instance.seller = self.request.user
        form.instance.status = 'active'
        
        # Validate price
        if form.cleaned_data['price'] < 0:
            form.add_error('price', 'Ensure this value is greater than or equal to 0')
            return self.form_invalid(form)
        
        try:
            with transaction.atomic():
                response = super().form_valid(form)
                
                # Handle images
                for i in range(4):
                    image_key = f'image_{i}'
                    if image_key in self.request.FILES:
                        ListingImage.objects.create(
                            listing=self.object,
                            image=self.request.FILES[image_key],
                            display_order=i,
                            is_primary=(i == 0)
                        )
                
                messages.success(self.request, 'Listing created successfully!')
                return response
                
        except Exception as e:
            messages.error(self.request, 'Error creating listing. Please try again.')
            return self.form_invalid(form)

class MyListingsView(LoginRequiredMixin, ListView):
    model = ProductListing
    template_name = 'listings/my_listings.html'
    context_object_name = 'listings'
    paginate_by = 9  # Show 9 listings per page
    ordering = ['-created_at']

    def get_queryset(self):
        return ProductListing.objects.filter(
            seller=self.request.user
        ).select_related(
            'category', 
            'category__main_category'
        ).prefetch_related(
            'images'
        ).order_by('-created_at')

class DeleteListingView(LoginRequiredMixin, DeleteView):
    model = ProductListing
    success_url = reverse_lazy('listings:my-listings')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.seller != request.user:
            return JsonResponse({'error': 'Not authorized'}, status=403)
        self.object.delete()
        return JsonResponse({'status': 'success'})

class ListingDetailView(DetailView):
    model = ProductListing
    template_name = 'listings/listing_detail.html'
    context_object_name = 'listing'

    def get_queryset(self):
        return ProductListing.objects.select_related(
            'seller',
            'category',
            'category__main_category'
        ).prefetch_related('images')