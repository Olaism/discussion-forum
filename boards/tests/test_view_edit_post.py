from django.contrib.auth import get_user_model
from django.forms import ModelForm
from django.test import TestCase
from django.urls import resolve, reverse

from ..models import Board, Post, Topic
from .utils import create_board, create_topic, create_post
from ..views import PostEditView

User = get_user_model()


class PostEditViewTestCase(TestCase):
    def setUp(self):
        """
        Base test case to be used in all `PostEditView` view tests
        """
        self.username = "testuser01"
        self.password = "testpassword01"
        user = User.objects.create_user(
            username=self.username,
            email="testuser01@example.com",
            password=self.password,
        )
        self.board = create_board("my board", "my board decription")
        self.topic = create_topic(
            board=self.board, 
            subject='my subject',
            starter=user
        )
        self.post = create_post(
            message="test message", 
            topic=self.topic, 
            author=user
        )
        self.url = reverse(
            "edit_post",
            kwargs={
                "pk": self.board.pk,
                "topic_pk": self.topic.pk,
                "post_pk": self.post.pk,
            },
        )


class LoginRequiredPostEditViewTest(PostEditViewTestCase):
    def test_redirection(self):
        login_url = reverse("login")
        response = self.client.get(self.url)
        self.assertRedirects(response, f"{login_url}?next={self.url}")


class UnauthorizedPostEditViewTest(PostEditViewTestCase):
    def setUp(self):
        super().setUp()
        username = "anonymous_user"
        password = "anonymouspwd"
        self.other_user = User.objects.create_user(
            username=username, email="anonymous@example.com", password=password
        )
        self.client.login(username=username, password=password)
        self.response = self.client.get(self.url)

    def test_status_code(self):
        """
        A topic should be edited only by the owner.
        An unauthorized user should return a 404 (not found) page
        """
        self.assertEquals(self.response.status_code, 404)


# class AuthorizedPostEditViewTests(PostEditViewTestCase):
#     def setUp(self):
#         super().setUp()
#         self.client.login(username=self.username, password=self.password)
#         self.response = self.client.get(self.url)

#     def test_status_code(self):
#         self.assertEquals(self.response.status_code, 200)

#     def test_resolve_url(self):
#         view = resolve(
#             f"/boards/{self.board.pk}/topics/{self.topic.pk}/posts/{self.post.pk}/edit/"
#         )
#         self.assertEquals(view.func.view_class, PostEditView)

#     def test_csrf(self):
#         self.assertContains(self.response, "csrfmiddlewaretoken")

#     def test_has_form(self):
#         form = self.response.context.get("form")
#         self.assertIsInstance(form, ModelForm)

#     def test_form_inputs(self):
#         """
#         The view must contain two inputs: csrf, message textarea
#         """
#         self.assertContains(self.response, "<input", 2)
#         self.assertContains(self.response, "<textarea", 1)

#     def test_template_used(self):
#         self.assertTemplateUsed(self.response, 'boards/edit_post.html')

#     def test_contains_breadcrumb(self):
#         home_url = reverse('home')
#         board_topics_url =reverse('board_topics', kwargs={'pk': self.board.pk})
#         topic_post_url = reverse('topic_posts', kwargs={
#             'pk': self.board.pk,
#             'topic_pk': self.topic.pk
#         })
#         self.assertContains(self.response, f'href="{home_url}"')
#         self.assertContains(self.response, f'href="{board_topics_url}"')
#         self.assertContains(self.response, f'href="{topic_post_url}"')


# class SuccessfulPostEditViewTest(PostEditViewTestCase):
#     def setUp(self):
#         super().setUp()
#         self.client.login(username=self.username, password=self.password)
#         self.response = self.client.post(self.url, data={"message": "edited message"})

#     def test_redirection(self):
#         """
#         A valid form submission should redirect the user
#         """
#         topic_posts_url = reverse(
#             "topic_posts", kwargs={"pk": self.board.pk, "topic_pk": self.topic.pk}
#         )
#         self.assertRedirects(self.response, topic_posts_url)

#     def test_post_changed(self):
#         self.post.refresh_from_db()
#         self.assertEquals(self.post.message, "edited message")


# class InvalidPostEditViewTests(PostEditViewTestCase):
#     def setUp(self):
#         """
#         Submit an empty dictionary to the `reply_topic` view
#         """
#         super().setUp()
#         self.client.login(username=self.username, password=self.password)
#         self.response = self.client.post(self.url, {})

#     def test_status_code(self):
#         """
#         An invalid form submission should return to the same page
#         """
#         self.assertEquals(self.response.status_code, 200)

#     def test_form_errors(self):
#         form = self.response.context.get("form")
#         self.assertTrue(form.errors)
