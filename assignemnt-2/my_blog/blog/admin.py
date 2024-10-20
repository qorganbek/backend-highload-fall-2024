from django.contrib import admin
from .models import User, Post, Comment, Tag, PostTag

class PostTagInline(admin.TabularInline):
    model = PostTag
    extra = 1 

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1 

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_date', 'comment_count')
    search_fields = ('title', 'content')
    list_filter = ('created_date', 'author')
    inlines = [PostTagInline, CommentInline]

class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_date')
    search_fields = ('content',)
    list_filter = ('created_date', 'author')

admin.site.register(Post, PostAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(User)
