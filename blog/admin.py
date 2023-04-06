from django.contrib import admin
from .models import Post


@admin.register(Post)
class BlogPostAdmin(admin.ModelAdmin):
    model = Post
    list_display = ('title', 'slug', 'status', 'publish', 'author')
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'author')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']
