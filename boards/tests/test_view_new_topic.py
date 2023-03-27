from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse, resolve

from ..forms import NewTopicForm
from ..models import (
    Board,
    Topic,
    Post
)
from ..views import new_topic

User = get_user_model()


class LoginRequiredNewTopicTest(TestCase):

    def test_redirection(self):
        board = Board.objects.create(
            name='Django board',
            description='All about django'
        )
        login_url = reverse('login')
        new_topic_url = reverse('new_topic', kwargs={'pk': board.pk})
        response = self.client.get(new_topic_url)
        self.assertRedirects(response, f"{login_url}?next={new_topic_url}")


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
        self.client.login(
            username='testuser01',
            password='testpassword01'
        )
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

    def test_new_topic_invalid_post_data(self):
        response = self.client.post(self.url, data={})
        form = response.context.get('form')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(form.errors)

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
