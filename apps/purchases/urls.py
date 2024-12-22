from django.urls import path
from . import views

app_name = 'purchases'

urlpatterns = [
    path('', views.PurchaseListView.as_view(), name='list'),
    path('<int:pk>/', views.PurchaseDetailView.as_view(), name='detail'),
] 