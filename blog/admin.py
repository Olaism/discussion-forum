from django.contrib import admin

from .models import Comment, Post


@admin.register(Post)
class BlogPostAdmin(admin.ModelAdmin):
    model = Post
    list_display = ('title', 'highlight', 'slug', 'status', 'publish', 'author')
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'author')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    model = Comment
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')
