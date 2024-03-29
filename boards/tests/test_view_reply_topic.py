from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import resolve, reverse

from ..forms import PostForm
from ..models import Board, Post, Topic
from ..views import reply_topic

User = get_user_model()


class ReplyTopicTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="testuser@example.com", password="testpassword"
        )
        self.board = Board.objects.create(
            name="test board", description="test board description"
        )
        self.topic = Topic.objects.create(
            subject="test subject", board=self.board, starter=self.user
        )
        Post.objects.create(
            message="test message", topic=self.topic, created_by=self.user
        )
        self.url = reverse(
            "reply_topic", kwargs={"pk": self.board.pk, "topic_pk": self.topic.pk}
        )


class LoginRequiredReplyTopicTest(ReplyTopicTestCase):
    def test_redirection(self):
        login_url = reverse("login")
        response = self.client.get(self.url)
        self.assertRedirects(response, f"{login_url}?next={self.url}")


class ReplyTopicTests(ReplyTopicTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username="testuser", password="testpassword")
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve(f"/boards/{self.board.pk}/topics/{self.topic.pk}/reply/")
        self.assertEquals(view.func, reply_topic)

    def test_csrf(self):
        self.assertContains(self.response, "csrfmiddlewaretoken")

    def test_has_form(self):
        form = self.response.context.get("form")
        self.assertIsInstance(form, PostForm)

    def test_form_inputs(self):
        self.assertContains(self.response, "<input", 2)
        self.assertContains(self.response, "<textarea", 1)

    def test_template_used(self):
        self.assertTemplateUsed(self.response, 'boards/reply_topic.html')

    def test_breadcrumbs(self):
        home_url = reverse('home')
        board_topics_url = reverse('board_topics', kwargs={'pk': self.board.pk})
        topic_post_url = reverse('topic_posts', kwargs={
            'pk': self.board.pk,
            'topic_pk': self.topic.pk,
        })
        self.assertContains(self.response, f'href="{home_url}"')
        self.assertContains(self.response, f'href="{board_topics_url}"')
        self.assertContains(self.response, f'href="{topic_post_url}"')

class SuccessfulReplyTopicTest(ReplyTopicTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username="testuser", password="testpassword")
        self.response = self.client.post(self.url, {"message": "test reply"})

    def test_redirection(self):
        """
        A valid form submission should redirect the user
        """
        url = reverse(
            "topic_posts", kwargs={"pk": self.board.pk, "topic_pk": self.topic.pk}
        )
        post = Post.objects.last()
        topic_posts_url = "{url}?page=1#{pk}".format(url=url, pk=post.pk)
        self.assertRedirects(self.response, topic_posts_url)

    def test_reply_created(self):
        self.assertEquals(Post.objects.count(), 2)


class InvalidReplyTopicTest(ReplyTopicTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username="testuser", password="testpassword")
        self.response = self.client.post(self.url, {})

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get("form")
        self.assertTrue(form.errors)
