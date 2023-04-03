from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import resolve, reverse

from ..models import Board, Post, Topic
from ..views import PostListView

User = get_user_model()


class TopicPostsTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(
            username="testuser", email="testuser@example.com", password="testpassword"
        )
        self.board = Board.objects.create(
            name="testboard", description="testboard description"
        )
        self.topic = Topic.objects.create(
            subject="test subject", board=self.board, starter=user
        )
        Post.objects.create(message="a test message", topic=self.topic, created_by=user)
        self.url = reverse(
            "topic_posts", kwargs={"pk": self.board.pk, "topic_pk": self.topic.pk}
        )


class LoginRequiredTopicPostsView(TopicPostsTestCase):
    def test_redirection(self):
        login_url = reverse("login")
        response = self.client.get(self.url)
        self.assertRedirects(response, f"{login_url}?next={self.url}")


class TopicPostsTests(TopicPostsTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(
            username="testuser",
            password="testpassword",
        )
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_resolve_url(self):
        view = resolve(f"/boards/{self.board.pk}/topics/{self.topic.pk}/")
        self.assertEquals(view.func.view_class, PostListView)
