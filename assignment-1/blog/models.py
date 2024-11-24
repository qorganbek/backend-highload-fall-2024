from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    id = models.AutoField(
        primary_key=True
    )  # Explicitly defining the id field (optional)
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the User model
    post = models.ForeignKey(
        Post, related_name="comments", on_delete=models.CASCADE
    )  # Link to the Post model
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.author} on {self.post}"
