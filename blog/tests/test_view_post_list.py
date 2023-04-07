from django.urls import reverse, resolve
from django.test import TestCase

from ..models import Post
from ..views import PostListView


class PostListViewTest(TestCase):

    def setUp(self):
        url = reverse('blog:post_list')
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/blog/')
        self.assertEquals(view.func.view_class, PostListView)
