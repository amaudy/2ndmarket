from django.views.generic import ListView
from apps.categories.models import MainCategory, SubCategory
from apps.listings.models import ProductListing
from django.db.models import Prefetch

class HomeView(ListView):
    model = ProductListing
    template_name = "core/home.html"
    context_object_name = 'listings'
    paginate_by = 12

    def get_queryset(self):
        queryset = ProductListing.objects.filter(
            status='active',
            is_available=True
        ).select_related(
            'category',
            'seller'
        ).prefetch_related('images')

        # Filter by category if provided
        category_id = self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        return queryset.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = MainCategory.objects.filter(
            is_active=True
        ).prefetch_related(
            Prefetch(
                'subcategory_set',
                queryset=SubCategory.objects.filter(is_active=True)
            )
        )
        context['selected_category'] = self.request.GET.get('category')
        return context 