from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import resolve, reverse

from .utils import (
    create_boards,
    create_topic,
    create_topics,
    create_posts
)
from ..models import Board, Topic
from ..views import TopicListView

User = get_user_model()


class BoardTopicsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )
        self.board = create_boards()
        self.topic = create_topic(board=self.board, subject='hello world', starter=self.user)
        self.url = reverse("board_topics", kwargs={"pk": self.board.pk})


class LoginRequiredBoardTopicsTest(BoardTopicsTestCase):
    def test_redirection(self):
        login_url = reverse("login")
        response = self.client.get(self.url)
        self.assertRedirects(response, f"{login_url}?next={self.url}")


class BoardTopicsTest(BoardTopicsTestCase):
    def setUp(self):
        super().setUp()
        url = reverse("board_topics", kwargs={"pk": self.board.pk})
        self.client.login(username="testuser", password="testpassword")
        self.response = self.client.get(url)

    def test_board_topics_view_success_code(self):
        self.assertEqual(200, self.response.status_code)

    def test_board_topics_view_not_found_status_code(self):
        url = reverse("board_topics", kwargs={"pk": 10})
        response = self.client.get(url)
        self.assertEqual(404, response.status_code)

    def test_board_topics_url_resolves_board_topics_view(self):
        view = resolve("/boards/1/")
        self.assertEqual(view.func.view_class, TopicListView)

    def test_template_used(self):
        self.assertTemplateUsed(self.response, 'boards/topics.html')

    def test_board_topics_view_contain_new_topic_links(self):
        homepage_url = reverse("home")
        new_topic_link = reverse("new_topic", kwargs={"pk": self.board.pk})
        self.assertContains(self.response, 'href="{0}"'.format(homepage_url))
        self.assertContains(self.response, 'href="{0}"'.format(new_topic_link))

    def test_get_last_ten_response(self):
        queryset = self.response.context.get('topics')
        self.assertQuerysetEqual(queryset, Topic.objects.order_by(
            '-last_updated')[:20])

    def test_view_is_not_paginated_for_19_or_below_topics(self):
        is_paginated = self.response.context.get('is_paginated')
        self.assertFalse(is_paginated)

    def test_view_is_paginated(self):
        create_topics(board=self.board, starter=self.user, num=60)
        url = reverse("board_topics", kwargs={"pk": self.board.pk})
        response = self.client.get(url)
        is_paginated = response.context.get('is_paginated')
        self.assertTrue(is_paginated)