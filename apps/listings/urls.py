from django.urls import path
from . import views

app_name = 'listings'

urlpatterns = [
    path('create/', views.CreateListingView.as_view(), name='create'),
    path('my-listings/', views.MyListingsView.as_view(), name='my-listings'),
    path('<int:pk>/delete/', views.DeleteListingView.as_view(), name='delete'),
    path('<int:pk>/', views.ListingDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.EditListingView.as_view(), name='edit'),
    path('images/<int:pk>/delete/', views.delete_listing_image, name='delete_image'),
    path('<int:pk>/comments/add/', views.AddCommentView.as_view(), name='add_comment'),
    path('comments/<int:pk>/edit/', views.EditCommentView.as_view(), name='edit_comment'),
    path('comments/<int:pk>/delete/', views.DeleteCommentView.as_view(), name='delete_comment'),
    path('<int:pk>/buy/', views.CreateOrderView.as_view(), name='buy'),
    path('orders/<int:pk>/confirm/', views.OrderConfirmView.as_view(), name='order_confirm'),
] 