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
from django.views.generic.edit import UpdateView
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied

class CreateListingView(LoginRequiredMixin, CreateView):
    model = ProductListing
    form_class = ProductListingForm
    template_name = 'listings/create_listing.html'
    success_url = reverse_lazy('listings:my-listings')

    def form_valid(self, form):
        print("\nCreate Listing Debug:")
        print(f"Form data: {form.cleaned_data}")
        print(f"Files: {self.request.FILES}")
        print(f"User: {self.request.user}")

        form.instance.seller = self.request.user
        form.instance.status = 'active'
        
        # Validate price
        if form.cleaned_data['price'] < 0:
            form.add_error('price', 'Price cannot be negative')
            return self.form_invalid(form)
        
        try:
            with transaction.atomic():
                response = super().form_valid(form)
                print(f"Listing created: {self.object.__dict__}")
                
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
                    print(f"Image {i} processed")
                
                messages.success(self.request, 'Listing created successfully!')
                return response
                
        except Exception as e:
            print(f"Error creating listing: {str(e)}")
            print(f"Exception type: {type(e)}")
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

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not obj.belongs_to_user(self.request.user):
            raise PermissionDenied
        return obj

    def delete(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
            self.object.delete()
            return HttpResponse(status=200)
        except PermissionDenied:
            return HttpResponse(status=403)
        except Exception as e:
            return HttpResponse(status=400)

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

class EditListingView(LoginRequiredMixin, UpdateView):
    model = ProductListing
    form_class = ProductListingForm
    template_name = 'listings/edit_listing.html'
    success_url = reverse_lazy('listings:my-listings')
    context_object_name = 'listing'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not obj.belongs_to_user(self.request.user):
            raise PermissionDenied
        return obj

    def get_queryset(self):
        return ProductListing.objects.filter(seller=self.request.user)

    def form_valid(self, form):
        try:
            with transaction.atomic():
                print("\nEdit Listing Debug:")
                print(f"Form valid: {form.is_valid()}")
                print(f"Form cleaned data: {form.cleaned_data}")
                print(f"Form errors: {form.errors}")
                print(f"Initial instance: {form.instance.__dict__}")

                self.object = form.save(commit=False)
                self.object.seller = self.request.user
                
                # Debug each field assignment
                print("\nField Assignments:")
                for field in ['title', 'description', 'price', 'condition', 'category', 'status', 'is_available']:
                    old_value = getattr(self.object, field)
                    setattr(self.object, field, form.cleaned_data[field])
                    new_value = getattr(self.object, field)
                    print(f"{field}: {old_value} -> {new_value}")

                self.object.save()
                print(f"\nFinal object: {self.object.__dict__}")

                messages.success(self.request, 'Listing updated successfully!')
                return super().form_valid(form)
                
        except Exception as e:
            print(f"Error in form_valid: {str(e)}")
            print(f"Exception type: {type(e)}")
            messages.error(self.request, 'Error updating listing. Please try again.')
            return self.form_invalid(form)

@login_required
def delete_listing_image(request, pk):
    if request.method == 'POST':
        image = get_object_or_404(ListingImage, pk=pk)
        # Check if user owns the listing
        if image.listing.seller != request.user:
            return JsonResponse({'error': 'Not authorized'}, status=403)
        
        image.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'error': 'Invalid method'}, status=405)