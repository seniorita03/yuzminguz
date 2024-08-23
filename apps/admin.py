from django.contrib import admin
from django.contrib.admin import StackedInline

from apps.models import Category, ProductImage, Product, Store


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    exclude = 'slug',


class ProductImageInline(StackedInline):
    model = ProductImage


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    exclude = 'slug',
    inlines = [ProductImageInline]


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    pass
