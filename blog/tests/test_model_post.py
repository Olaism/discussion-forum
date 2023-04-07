from django.contrib.auth import get_user_model
from django.template.defaultfilters import slugify
from django.test import TestCase

from ..models import Post

User = get_user_model()


class PostModelTest(TestCase):

    def setUp(self):
        user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )
        self.post = Post.objects.create(
            title='post title',
            author=user,
            body='test body',
            status='published'
        )

    def test_string_representation(self):
        self.assertEqual(str(self.post), self.post.title)

    def test_slug(self):
        self.assertEqual(self.post.slug, slugify(self.post.title))

    def test_absolute_url(self):
        year = self.post.publish.year
        month = self.post.publish.strftime('%m')
        day = self.post.publish.strftime('%d')
        slug = self.post.slug
        url = f'/blog/{year}/{month}/{day}/{slug}/'
        self.assertEquals(self.post.get_absolute_url(), url)
