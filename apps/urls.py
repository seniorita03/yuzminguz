from django.contrib.auth.views import LogoutView
from django.urls import path

from apps.views import HomeView, ProductListView, ProductDetailView, ProfileFormView, AloqaView, MarketView, StreamView, \
    StatisticsView, PaymentView, DashboardView, CustomLoginView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('accounts/login/', CustomLoginView.as_view(), name='login'),
    path('product-list', ProductListView.as_view(), name='product-list'),
    path('product-detail/<str:slug>', ProductDetailView.as_view(), name='detail'),
    path('aloqa/', AloqaView.as_view(), name='aloqa'),
    path('profile', ProfileFormView.as_view(), name='profile'),
    path('dashbord', DashboardView.as_view(), name='dashboard'),
    path('market', MarketView.as_view(), name='market'),
    path('stream',StreamView.as_view(), name='stream'),
    path('statistics',StatisticsView.as_view(), name='statistics'),
    path('payment', PaymentView.as_view(), name='payment'),
    path('logout', LogoutView.as_view(), name='logout'),

]

