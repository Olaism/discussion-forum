from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse, resolve

from ..models import (
    Board,
    Topic
)
from ..views import board_topics

User = get_user_model()


class LoginRequiredBoardTopicsTest(TestCase):

    def test_redirection(self):
        board = Board.objects.create(
            name='example',
            description='An example description'
        )
        login_url = reverse('login')
        board_topics_url = reverse('board_topics', kwargs={'pk': board.pk})
        response = self.client.get(board_topics_url)
        self.assertRedirects(response, f"{login_url}?next={board_topics_url}")


class BoardTopicsTest(TestCase):

    def setUp(self):
        User.objects.create_user(
            username='testuser01',
            email='testuser01@gmail.com',
            password='testpassword01'
        )
        self.board = Board.objects.create(
            name='Olaism', description='Olaism bored')
        url = reverse('board_topics', kwargs={'pk': self.board.pk})
        self.client.login(
            username='testuser01',
            password='testpassword01'
        )
        self.response = self.client.get(url)

    def test_board_topics_view_success_code(self):
        self.assertEqual(200, self.response.status_code)

    def test_board_topics_view_not_found_status_code(self):
        url = reverse('board_topics', kwargs={'pk': 10})
        response = self.client.get(url)
        self.assertEqual(404, response.status_code)

    def test_board_topics_url_resolves_board_topics_view(self):
        view = resolve('/boards/1/')
        self.assertEqual(view.func, board_topics)

    def test_board_topics_view_contain_new_topic_links(self):
        homepage_url = reverse('home')
        new_topic_link = reverse('new_topic', kwargs={'pk': self.board.pk})
        self.assertContains(
            self.response,
            'href="{0}"'.format(homepage_url)
        )
        self.assertContains(self.response, 'href="{0}"'.format(new_topic_link))
