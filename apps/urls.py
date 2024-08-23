from django.urls import path

from apps.views import HomeView, ProductListView, ProductDetailView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('product-list', ProductListView.as_view(), name='product-list'),
    path('product-detail/<str:slug>', ProductDetailView.as_view(), name='detail'),
]

