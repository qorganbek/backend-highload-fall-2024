from django.shortcuts import render, get_object_or_404, redirect
from .custom_queries import get_post_with_comments
from .models import Post, Comment
from django.views.decorators.cache import cache_page
from django.core.cache import cache


def get_post_by_id(request, post_id):
    post = get_post_with_comments(post_id)
    return render(request, "blog/post_with_comments.html", {"post": post})


@cache_page(60)
def get_posts(request):
    posts = Post.objects.all().order_by("-created_date")
    return render(request, "blog/post_list.html", {"posts": posts})


def add_comment(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == "POST":
        content = request.POST.get("content")
        Comment.objects.create(post=post, author=request.user, content=content)

        cache_key = f"post_{post_id}_comment_count"
        cache.delete(cache_key)

    return redirect("post_detail", post_id=post_id)
