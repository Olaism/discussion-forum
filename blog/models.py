from django.conf import settings
from django.db import models
from django.utils import timezone


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=255)
    slug = models.SlugField(
        max_length=255,
        unique_for_date='publish'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='blog_posts',
        on_delete=models.CASCADE
    )
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=100,
        choices=STATUS_CHOICES,
        default='draft'
    )

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title
