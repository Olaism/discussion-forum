from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse

from ..forms import SignupForm
from ..views import signup


class SignupTests(TestCase):
    def setUp(self):
        url = reverse("signup")
        self.response = self.client.get(url)

    def test_signup_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_signup_url_resolves_signup_view(self):
        view = resolve("/accounts/signup/")
        self.assertEquals(view.func, signup)

    def test_csrf(self):
        self.assertContains(self.response, "csrfmiddlewaretoken")

    def test_contains_forms(self):
        form = self.response.context.get("form")
        self.assertIsInstance(form, SignupForm)

    def test_form_inputs(self):
        """ """
        self.assertContains(self.response, "<input", 6)
        self.assertContains(self.response, 'type="text"', 1)
        self.assertContains(self.response, 'type="email"', 1)
        self.assertContains(self.response, 'type="password"', 2)


class SuccessfulSignupTests(TestCase):
    def setUp(self):
        url = reverse("signup")
        data = {
            "username": "testme",
            "email": "testme@gmail.com",
            "password1": "testmepassword",
            "password2": "testmepassword",
        }
        self.response = self.client.post(url, data)
        self.home_url = reverse("home")

    def test_redirection(self):
        """
        A valid form submission should redirect the user to the home page
        """
        login_url = reverse("login")
        self.assertRedirects(self.response, login_url)

    def test_user_creation(self):
        self.assertTrue(User.objects.exists())


class InvalidSignupTests(TestCase):
    def setUp(self):
        url = reverse("signup")
        self.response = self.client.post(url, {})

    def test_signup_status_code(self):
        """
        An invalid form submission should return to the same page
        """
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get("form")
        self.assertTrue(form.errors)

    def test_dont_create_user(self):
        self.assertFalse(User.objects.exists())
