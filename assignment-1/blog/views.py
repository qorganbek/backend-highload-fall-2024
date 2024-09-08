from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from . import models
from .forms import BlogForm, CommentForm
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import Post


def home(request):
    return HttpResponse("Hello, Blog!")


def blog_list(request):
    blogs = models.Post.objects.all()
    paginator = Paginator(blogs, 5)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "blog/blog_list.html", {"page_obj": page_obj})


def blog_detail(request, id):
    blog = get_object_or_404(Post, id=id)
    comments = blog.comments.all()  # Get all comments related to this blog post

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = blog
            comment.author = request.user  # Assign the logged-in user as the author
            comment.save()
            return redirect('blog_detail', id=blog.id)
    else:
        form = CommentForm()

    return render(request, 'blog/blog_detail.html', {'blog': blog, 'comments': comments, 'form': form})


@login_required
def create_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog_list')
    else:
        form = BlogForm()

    return render(request, 'blog/create_blog.html', {'form': form})


@login_required
def edit_blog(request, id):
    blog = get_object_or_404(models.Post, id=id)
    if str(blog.author) != str(request.user):
        return HttpResponseForbidden("You are not allowed to edit this post.")

    if request.method == 'POST':
        form = BlogForm(request.POST, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('blog_detail', id=blog.id)
    else:
        form = BlogForm(instance=blog)

    return render(request, 'blog/edit_blog.html', {'form': form, 'blog': blog})


@login_required
def delete_blog(request, id):
    blog = get_object_or_404(models.Post, id=id)

    if str(blog.author) != str(request.user):
        return HttpResponseForbidden("You are not allowed to delete this post.")

    if request.method == 'POST':
        blog.delete()
        return redirect('blog_list')

    return render(request, 'blog/delete_blog.html', {'blog': blog})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('blog_list')
    else:
        form = UserCreationForm()

    return render(request, 'blog/register.html', {'form': form})