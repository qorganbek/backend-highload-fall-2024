from rest_framework import viewsets
from django.core.cache import cache

from src.settings import CACHE_TTL
from main.models import Category, Product, Order
from main.serializers import CategorySerializer, ProductSerializer, OrderSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.prefetch_related("products")
    serializer_class = CategorySerializer

    def get_queryset(self):
        cache_key = "category_list"
        categories = cache.get(cache_key)

        if not categories:
            categories = Category.objects.prefetch_related("products")
            cache.set(cache_key, categories, timeout=CACHE_TTL)

        return categories


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related("category")
    serializer_class = ProductSerializer

    def get_queryset(self):
        cache_key = "product_list"
        products = cache.get(cache_key)

        if not products:
            products = Product.objects.select_related("category")
            cache.set(cache_key, products, timeout=CACHE_TTL)

        return products


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.select_related("product").prefetch_related(
        "product__category"
    )
    serializer_class = OrderSerializer

    def get_queryset(self):
        cache_key = "order_list"
        orders = cache.get(cache_key)

        if not orders:
            orders = Order.objects.select_related("product").prefetch_related(
                "product__category"
            )
            cache.set(cache_key, orders, timeout=CACHE_TTL)

        return orders
