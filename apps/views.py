import re

from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, FormView, TemplateView

from apps.forms import OrderForm, ProfileForm
from apps.models import Category, Product, User


class HomeView(ListView):
    queryset = Category.objects.all()
    template_name = 'apps/main.html'
    context_object_name = 'categories'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['products'] = Product.objects.all()
        data['popular_products'] = Product.objects.order_by('order_count')[:8]
        return data


class ProductListView(ListView):
    queryset = Product.objects.all()
    template_name = 'apps/product/product-list.html'
    context_object_name = 'products'

    def get_queryset(self):
        cat_slug = self.request.GET.get('category')
        query = super().get_queryset()
        if cat_slug:
            query = query.filter(category__slug=cat_slug)
        return query

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['categories'] = Category.objects.all()
        return data


class ProductDetailView(DetailView, FormView):
    form_class = OrderForm
    queryset = Product.objects.all()
    template_name = 'apps/product/product-detail.html'
    context_object_name = 'product'
    slug_url_kwarg = 'slug'

    # def form_valid(self, form):
    #     if form.is_valid():
    #         form = form.save(commit=False)
    #         form.user = self.request.user
    #         form.save()
    #     return render(self.request, 'apps/order/order.html', {'form': form})

class AloqaView(TemplateView):
    template_name = 'apps/kabinet/aloqa.html'

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'apps/kabinet/profile/dashboard.html'

class MarketView(LoginRequiredMixin, TemplateView):
    template_name = 'apps/kabinet/profile/market.html'


class StreamView(LoginRequiredMixin, TemplateView):
    template_name = 'apps/kabinet/profile/stream.html'


class StatisticsView(LoginRequiredMixin, TemplateView):
    template_name = 'apps/kabinet/profile/statistics.html'


class PaymentView(LoginRequiredMixin, TemplateView):
    template_name = 'apps/kabinet/profile/payment.html'

class CustomLoginView(TemplateView):
    template_name = 'apps/auth/login.html'

    def post(self, request, *args, **kwargs):
        phone_number = re.sub(r'\D', '', request.POST.get('phone_number', ''))
        user = User.objects.filter(phone_number=phone_number).first()

        if len(phone_number) < 10:
            context = {
                "messages_error": ["Invalid phone number"]
            }
            return render(request, self.template_name, context)
            # send_email

        if not user:
            user = User.objects.create_user(phone_number=phone_number, password=request.POST.get('password'))
            login(request, user)
            return redirect('home')

        user = authenticate(request, username=user.phone_number, password=request.POST.get('password'))
        if user:
            login(request, user)
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            context = {
                "messages_error": ["Invalid password"]
            }
            return render(request, self.template_name, context)


class ProfileFormView(FormView):
    form_class = ProfileForm
    template_name = 'apps/kabinet/profile1.html'

    def form_valid(self, form):
        data = form.save(commit=False)
        print(data)

    def form_invalid(self, form):
        data = form.errors
        print(data)

