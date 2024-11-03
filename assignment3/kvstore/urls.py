from django.urls import path
from .views import KeyValueStoreView

urlpatterns = [
    path('kv/<str:key>/', KeyValueStoreView.as_view(), name='key_value'),
    path('kv/', KeyValueStoreView.as_view(), name='create_or_update'),
]