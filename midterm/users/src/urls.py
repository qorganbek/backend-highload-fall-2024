from django.contrib import admin
from django.urls import path, include
from user.urls import urlpatterns as user_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('auth/', include(user_urls))
]
