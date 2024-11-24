from .models import Post
from django.core.cache import cache
from .models import Post, Comment


def get_post_with_comments(post_id):
    return Post.objects.prefetch_related("comment_set").get(id=post_id)


def get_comment_count(post_id):
    cache_key = f"post_{post_id}_comment_count"
    comment_count = cache.get(cache_key)

    if comment_count is None:
        comment_count = Comment.objects.filter(post_id=post_id).count()
        cache.set(cache_key, comment_count, timeout=60)

    return comment_count
