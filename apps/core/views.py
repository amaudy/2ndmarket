from django.views.generic import TemplateView
from apps.categories.models import MainCategory

class HomeView(TemplateView):
    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = MainCategory.objects.filter(is_active=True)[:6]
        return context 