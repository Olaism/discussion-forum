from django.contrib.auth import get_user_model
from django.urls import reverse, resolve
from django.test import TestCase

from ..models import Post
from ..views import PostDetailView

User = get_user_model()


class PostDetailTests(TestCase):

    def setUp(self):
        user = User.objects.create_user(
            username='testme',
            email='testme@example.com',
            password='testmepassword'
        )

        self.published_post = Post.objects.create(
            title='published blog post',
            author=user,
            body='test body',
            status='published'
        )

        self.unpublished_post = Post.objects.create(
            title='draft blog post',
            author=user,
            body='test body',
        )

        self.response = self.client.get(self.published_post.get_absolute_url())

    def test_published_post_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_unpublished_post_view_status_code(self):
        # A draft status post should return 404 (not found)
        response = self.client.get(self.unpublished_post.get_absolute_url())
        self.assertEquals(response.status_code, 404)

    def test_view_function(self):
        year = self.published_post.publish.year
        month = self.published_post.publish.month
        day = self.published_post.publish.day
        slug = self.published_post.slug
        view = resolve(f"/blog/{year}/{month}/{day}/{slug}/")
        self.assertEquals(view.func.view_class, PostDetailView)

    def test_template_used(self):
        self.assertTemplateUsed(self.response, '_base.html')
        self.assertTemplateUsed(self.response, 'blog/post/detail.html')
