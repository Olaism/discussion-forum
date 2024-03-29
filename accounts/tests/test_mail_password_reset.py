from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class PasswordResetMailTests(TestCase):
    def setUp(self):
        User.objects.create_user(
            username="testuser", email="testuser@gmail.com", password="testpassword"
        )
        self.response = self.client.post(
            reverse("password_reset"), {"email": "testuser@gmail.com"}
        )
        self.email = mail.outbox[0]

    def test_email_subject(self):
        self.assertEqual(
            "[Django Boards] Please reset your password", self.email.subject
        )

    def test_email_body(self):
        context = self.response.context
        token = context.get("token")
        uid = context.get("uid")
        password_reset_token_url = reverse(
            "password_reset_confirm", kwargs={"uidb64": uid, "token": token}
        )
        self.assertIn(password_reset_token_url, self.email.body)
        self.assertIn("testuser", self.email.body)
        self.assertIn("testuser@gmail.com", self.email.body)

    def test_email_to(self):
        self.assertEqual(
            [
                "testuser@gmail.com",
            ],
            self.email.to,
        )
