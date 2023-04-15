from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import resolve, reverse

from ..models import Board
from ..views import BoardListView
from .utils import (
    create_boards,
    create_topics,
    create_posts
)

User = get_user_model()


class LoginRequiredHomeViewTest(TestCase):
    """
    redirects unauthenticated user back to login
    """
    def test_redirection(self):
        login_url = reverse("login")
        home_url = reverse("home")
        response = self.client.get(home_url)
        self.assertRedirects(response, f"{login_url}?next={home_url}")

class NoBoardHomeTest(TestCase):

    def test_no_board_alert(self):
        user = User.objects.create_user(
            username="testuser", email="testuser@example.com", password="testpassword"
        )
        url = reverse('home')
        self.client.login(
            username='testuser',
            password='testpassword',
        )
        response = self.client.get(url)
        self.assertContains(response, 'No board available')

class HomeTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="testuser@example.com", password="testpassword"
        )
        self.board = create_boards(2)
        topic = create_topics(board=self.board, starter=self.user) # create 20 topics under the last created board
        create_posts(topic=topic, author=self.user) # create 20 post under the topic
        url = reverse("home")
        self.client.login(username="testuser", password="testpassword")
        self.response = self.client.get(url)

    def test_home_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        view = resolve("/boards/")
        self.assertEquals(view.func.view_class, BoardListView)

    def test_template_used(self):
        self.assertTemplateUsed(self.response, 'boards/home.html')

    def test_home_view_contains_links_to_topics_page(self):
        board_topics_url = reverse("board_topics", kwargs={"pk": self.board.pk})
        self.assertContains(self.response, 'href="{0}"'.format(board_topics_url))

    def test_view_contains_neccessary_info(self):
        last_post = self.board.get_last_post()
        self.assertContains(self.response, self.board.topics.count()) # check if view contains the total topics count
        self.assertContains(self.response, self.board.description) # check if view contains the board description
        self.assertContains(self.response, self.board.get_posts_count()) # check if view contains the number of post for a board
        self.assertContains(self.response, self.user.username) # check if view contains the aunthenticated user
        self.assertContains(self.response, last_post.created_by.username) # check if view contains the author of the last post username
        self.assertContains(self.response, f"/boards/{last_post.topic.board.pk}/topics/{last_post.topic.pk}") # check if view contains the last post link