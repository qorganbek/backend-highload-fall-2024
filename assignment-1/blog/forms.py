from django import forms
from .models import Post, Comment


class BlogForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "content", "author")


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
        widgets = {
            "text": forms.Textarea(attrs={"rows": 4, "cols": 40}),
        }
