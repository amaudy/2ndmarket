from django.views.generic import DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib import messages
from .models import UserProfile
from .forms import UserProfileForm

class ProfileDetailView(DetailView):
    model = User
    template_name = 'accounts/profile_detail.html'
    context_object_name = 'profile_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context['active_listings'] = user.productlisting_set.filter(
            status='active'
        ).select_related('category').prefetch_related('images')[:6]
        context['sold_listings'] = user.productlisting_set.filter(
            status='sold'
        ).select_related('category').prefetch_related('images')[:6]
        return context

class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'accounts/profile_edit.html'
    def get_success_url(self):
        return reverse_lazy('accounts:profile_detail', kwargs={'pk': self.request.user.pk})

    def get_object(self, queryset=None):
        return self.request.user.userprofile

    def form_valid(self, form):
        messages.success(self.request, 'Profile updated successfully!')
        return super().form_valid(form) 