from rest_framework.routers import DefaultRouter
from . import views

r = DefaultRouter()

r.register('categories', views.CategoryViewSet)
r.register('products', views.ProductViewSet)
r.register('orders', views.OrderViewSet)
