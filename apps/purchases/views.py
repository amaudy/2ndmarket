from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.listings.models import Order

class PurchaseListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'purchases/list.html'
    context_object_name = 'orders'
    paginate_by = 10

    def get_queryset(self):
        return Order.objects.filter(
            buyer=self.request.user
        ).select_related(
            'listing',
            'listing__seller',
            'listing__category'
        ).prefetch_related(
            'listing__images'
        ).order_by('-created_at')

class PurchaseDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'purchases/detail.html'
    context_object_name = 'order'

    def get_queryset(self):
        return Order.objects.filter(
            buyer=self.request.user
        ).select_related(
            'listing',
            'listing__seller',
            'listing__category'
        ).prefetch_related(
            'listing__images'
        ) 