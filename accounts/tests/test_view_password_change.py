from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import (PasswordChangeDoneView,
                                       PasswordChangeView)
from django.test import TestCase
from django.urls import resolve, reverse

User = get_user_model()


class PasswordChangeTest(TestCase):
    def setUp(self):
        User.objects.create_user(
            username="testuser", email="testuser@gmail.com", password="testpassword"
        )
        url = reverse("password_change")
        self.client.login(username="testuser", password="testpassword")
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve("/accounts/password_change/")
        self.assertEquals(view.func.view_class, PasswordChangeView)

    def test_csrf(self):
        self.assertContains(self.response, "csrfmiddlewaretoken")

    def test_has_form(self):
        form = self.response.context.get("form")
        self.assertIsInstance(form, PasswordChangeForm)

    def test_form_inputs(self):
        self.assertContains(self.response, "<input", 4)
        self.assertContains(self.response, 'type="password"')


class LoginRequiredPasswordChangeTest(TestCase):
    def test_redirection(self):
        url = reverse("password_change")
        login_url = reverse("login")
        response = self.client.get(url)
        self.assertRedirects(response, f"{login_url}?next={url}")


class PasswordChangeTestCase(TestCase):
    def setUp(self, data={}):
        self.user = User.objects.create_user(
            username="testuser", email="testuser@gmail.com", password="oldtestpassword"
        )
        self.url = reverse("password_change")
        self.client.login(username="testuser", password="oldtestpassword")
        self.response = self.client.post(self.url, data)


class SuccessfulPasswordChangeTest(PasswordChangeTestCase):
    def setUp(self):
        super().setUp(
            {
                "old_password": "oldtestpassword",
                "new_password1": "newtestpassword",
                "new_password2": "newtestpassword",
            }
        )

    def test_redirection(self):
        self.assertRedirects(self.response, reverse("password_change_done"))

    def test_password_changed(self):
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("newtestpassword"))

    def test_user_authentication(self):
        """
        Create a new request to an arbitrary page.
        The resulting response should now have an `user` to its context, after a successful sign up.
        """
        response = self.client.get(reverse("home"))
        user = response.context.get("user")
        self.assertTrue(user.is_authenticated)


class InvalidPasswordChangeTest(PasswordChangeTestCase):
    def test_status_code(self):
        """
        An invalid form submission should return to the same page
        """
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get("form")
        self.assertTrue(form.errors)

    def test_didnt_change_password(self):
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("oldtestpassword"))


class PasswordChangeDoneTest(TestCase):
    def setUp(self):
        User.objects.create_user(
            username="testuser", email="testuser@gmail.com", password="testpassword"
        )
        url = reverse("password_change_done")
        self.client.login(username="testuser", password="testpassword")
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve("/accounts/password_change/done/")
        self.assertEquals(view.func.view_class, PasswordChangeDoneView)
