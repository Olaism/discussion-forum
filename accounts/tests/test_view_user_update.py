from django.contrib.auth import get_user_model
from django.forms import ModelForm
from django.test import TestCase
from django.urls import resolve, reverse

from ..views import UserUpdateView

User = get_user_model()


class UserUpdateViewTestCase(TestCase):
    def setUp(self):
        self.username = "testuser"
        self.password = "testpassword"
        self.user = User.objects.create_user(
            username=self.username, email="testmail@example.com", password=self.password
        )
        self.url = reverse("my_account")


class LoginRequiredUserUpdateViewTest(UserUpdateViewTestCase):
    def test_redirection(self):
        login_url = reverse("login")
        response = self.client.get(self.url)
        self.assertRedirects(
            response, "{login}?next={url}".format(login=login_url, url=self.url)
        )


class UserUpdateViewTest(UserUpdateViewTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_resolved_url(self):
        view = resolve("/accounts/")
        self.assertEquals(view.func.view_class, UserUpdateView)

    def test_csrf(self):
        self.assertContains(self.response, "csrfmiddlewaretoken")

    def test_has_form(self):
        form = self.response.context.get("form")
        self.assertIsInstance(form, ModelForm)

    def test_form_inputs(self):
        self.assertContains(self.response, "<input", 4)
        self.assertContains(self.response, 'type="email"', 1)


class SuccessfulUserUpdateViewTest(UserUpdateViewTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(
            self.url,
            {
                "first_name": "tester",
                "last_name": "john",
                "email": "updatedmail@user.com",
            },
        )

    def test_redirection(self):
        self.assertRedirects(self.response, reverse("my_account"))

    def test_user_update(self):
        self.user.refresh_from_db()
        self.assertEquals(self.user.first_name, "tester")
        self.assertEquals(self.user.last_name, "john")
        self.assertEquals(self.user.email, "updatedmail@user.com")


class NoInputUserUpdateViewTest(UserUpdateViewTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.url, {})

    def test_redirection(self):
        """
        An empty form submission should still submit successfully
        """
        self.assertRedirects(self.response, reverse("my_account"))

    def test_no_user_update(self):
        self.user.refresh_from_db()
        self.assertEquals(self.user.first_name, "")
        self.assertEquals(self.user.last_name, "")
        self.assertEquals(self.user.email, "")
