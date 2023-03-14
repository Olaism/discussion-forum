from django.test import TestCase
from django.urls import reverse, resolve

from .models import Board
from .views import (
    home,
    board_topics
)


class BaseTestView(TestCase):

    def test_url_redirect_to_home_view(self):
        home_url = reverse('home')
        response = self.client.get('/')
        self.assertRedirects(response, home_url)


class HomeTest(TestCase):

    def setUp(self):
        self.board = Board.objects.create(
            name='Django Board',
            description='All you need to need about django.'
        )
        url = reverse('home')
        self.response = self.client.get(url)

    def test_home_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        view = resolve('/boards/')
        self.assertEquals(view.func, home)

    def test_home_view_contains_links_to_topics_page(self):
        board_topics_url = reverse(
            'board_topics',
            kwargs={'pk': self.board.pk}
        )
        self.assertContains(
            self.response,
            'href="{0}"'.format(board_topics_url)
        )


class BoardTopicsTest(TestCase):

    def setUp(self):
        self.board = Board.objects.create(
            name='Olaism', description='Olaism bored')

    def test_board_topics_view_success_code(self):
        url = reverse('board_topics', kwargs={'pk': self.board.pk})
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)

    def test_board_topics_view_not_found_status_code(self):
        url = reverse('board_topics', kwargs={'pk': 10})
        response = self.client.get(url)
        self.assertEqual(404, response.status_code)

    def test_board_topics_url_resolves_board_topics_view(self):
        view = resolve('/boards/1/')
        self.assertEqual(view.func, board_topics)

    def test_board_topics_view_contains_links_back_to_homepage(self):
        board_topics_url = reverse(
            'board_topics', kwargs={'pk': self.board.pk}
        )
        response = self.client.get(board_topics_url)
        homepage_url = reverse('home')
        self.assertContains(
            response,
            'href="{0}"'.format(homepage_url)
        )
