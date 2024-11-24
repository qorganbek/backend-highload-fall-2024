from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.home),
    path("blogs/", views.blog_list, name="blog_list"),
    path("blogs/<int:id>/", views.blog_detail, name="blog_detail"),
    path("create/", views.create_blog, name="create_blog"),
    path("blogs/<int:id>/edit/", views.edit_blog, name="blog_edit"),
    path("blogs/<int:id>/delete/", views.delete_blog, name="blog_delete"),
    path("register/", views.register, name="register"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="blog/login.html"),
        name="login",
    ),
    path(
        "logout/", auth_views.LogoutView.as_view(next_page="blog_list"), name="logout"
    ),
]
