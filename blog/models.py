from django.conf import settings
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils import timezone

from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=100)
    highlight = models.CharField(max_length=255)
    tags = TaggableManager()
    slug = models.SlugField(
        max_length=255,
        unique_for_date='publish',
        null=True
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
        indexes = [
            models.Index(fields=['-publish']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={
            'year': self.publish.year,
            'month': self.publish.strftime('%m'),
            'day': self.publish.strftime('%d'),
            'slug': self.slug
        })

    objects = models.Manager()  # The default manager
    published = PublishedManager()  # Custom Mnagaer


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)
        indexes = [
            models.Index(fields=['created',])
        ]

    def __str__(self):
        return 'comment by {} on {}'.format(self.name, self.created)
