from django.urls import path
from . import views

app_name = 'listings'

urlpatterns = [
    path('create/', views.CreateListingView.as_view(), name='create'),
    path('my-listings/', views.MyListingsView.as_view(), name='my-listings'),
] 