from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse, resolve

from .forms import NewTopicForm
from .models import (
    Board,
    Topic
)
from .views import (
    home,
    board_topics,
    new_topic,
)

User = get_user_model()


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
        url = reverse('board_topics', kwargs={'pk': self.board.pk})
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


class NewTopicTests(TestCase):

    def setUp(self):
        self.board = Board.objects.create(
            name='Django board',
            description='All about django'
        )
        User.objects.create_user(
            username='testuser01',
            email='testuser01@gmail.com',
            password='testpassword01'
        )
        self.url = reverse('new_topic', kwargs={'pk': self.board.pk})
        self.response = self.client.get(self.url)

    def test_new_topic_view_success_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_new_topic_view_not_found_status_code(self):
        url = reverse('new_topic', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_new_topic_url_resolves_new_topic_test(self):
        view = resolve('/boards/{0}/new/'.format(self.board.pk))
        self.assertEqual(view.func, new_topic)

    def test_new_topic_view_contains_link_back_to_board_topics_view(self):
        board_topics_url = reverse(
            'board_topics', kwargs={'pk': self.board.pk})
        self.assertContains(
            self.response,
            'href="{0}"'.format(board_topics_url)
        )

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, NewTopicForm)

    def test_csrf_presence(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_new_topic_valid_post_data(self):
        data = {
            'subject': 'A subject for you.',
            'message': 'A message for everyone'
        }
        response = self.client.post(self.url, data=data)
        self.assertTrue(Topic.objects.exists())
        self.assertTrue(Post.objects.exists())

    def test_new_topic_invalid_post_sata(self):
        response = self.client.get(self.url)
        form = response.context.get('form')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(form.error)

    def test_new_post_invalid_data_with_empty_fields(self):
        data = {
            'subject': 'My new subject',
            'messsage': "Another message"
        }
        response = self.client.post(
            self.url,
            data=data
        )
        self.assertEqual(self.response.status_code, 200)
        self.assertFalse(Topic.objects.exists())
        self.assertFalse(Topic.objects.exists())
