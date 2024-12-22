from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('user/<int:pk>/', views.ProfileDetailView.as_view(), name='profile_detail'),
    path('settings/profile/', views.ProfileEditView.as_view(), name='profile_edit'),
] 