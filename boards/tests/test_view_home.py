from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import resolve, reverse

from ..models import Board
from ..views import BoardListView

User = get_user_model()


class LoginRequiredHomeViewTest(TestCase):
    def test_redirection(self):
        login_url = reverse("login")
        home_url = reverse("home")
        response = self.client.get(home_url)
        self.assertRedirects(response, f"{login_url}?next={home_url}")


class HomeTest(TestCase):
    def setUp(self):
        User.objects.create_user(
            username="testuser", email="testuser@example.com", password="testpassword"
        )
        self.board = Board.objects.create(
            name="Django Board", description="All you need to need about django."
        )
        url = reverse("home")
        self.client.login(username="testuser", password="testpassword")
        self.response = self.client.get(url)

    def test_home_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        view = resolve("/boards/")
        self.assertEquals(view.func.view_class, BoardListView)

    def test_home_view_contains_links_to_topics_page(self):
        board_topics_url = reverse("board_topics", kwargs={"pk": self.board.pk})
        self.assertContains(self.response, 'href="{0}"'.format(board_topics_url))
