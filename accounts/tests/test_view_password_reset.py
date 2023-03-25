from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    PasswordResetForm,
    SetPasswordForm
)
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)
from django.core import mail
from django.urls import reverse, resolve
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.test import TestCase


User = get_user_model()


class PasswordResetTests(TestCase):

    def setUp(self):
        url = reverse('password_reset')
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/accounts/password_reset/')
        self.assertEquals(view.func.view_class, PasswordResetView)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, PasswordResetForm)

    def test_form_inputs(self):
        """
        This view must contain two inputs: csrf and email
        """
        self.assertContains(self.response, '<input', 2)
        self.assertContains(self.response, 'type="email"', 1)


class SuccessfulPasswordResetTests(TestCase):

    def setUp(self):
        email = 'testuser@email.com'
        User.objects.create_user(
            username='testuser',
            email=email,
            password='testpassword'
        )
        url = reverse('password_reset')
        self.response = self.client.post(url, {'email': email})

    def test_redirection(self):
        """
        A valid form submission should redirect the user to 
        `password_reset_done` view
        """
        url = reverse('password_reset_done')
        self.assertRedirects(self.response, url)

    def test_send_password_reset_email(self):
        self.assertEqual(1, len(mail.outbox))


class InvalidPasswordResetTests(TestCase):

    def setUp(self):
        url = reverse('password_reset')
        self.response = self.client.post(url, {
            'email': 'donotexists@gmail.com'
        })

    def test_redirection(self):
        """
        Even an invalid emails in the database should redirect the user
        to `password_reset_done` view
        """
        url = reverse('password_reset_done')
        self.assertRedirects(self.response, url)

    def test_no_reset_email_sent(self):
        self.assertEqual(0, len(mail.outbox))


class PasswordResetDoneTests(TestCase):

    def setUp(self):
        url = reverse('password_reset_done')
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/accounts/password_reset/done/')
        self.assertEquals(view.func.view_class, PasswordResetDoneView)


class PasswordResetConfirmTests(TestCase):

    def setUp(self):
        user = User.objects.create_user(
            username='testuser',
            email='testuser@gmail.com',
            password='testpassword'
        )

        '''
        create a valid password reset token
        based on how django creates the token internally:
        https://github.com/django/django/blob/main/django/contrib/auth/forms.py
        '''

        self.uid = urlsafe_base64_encode(force_bytes(user.pk))
        self.token = default_token_generator.make_token(user)

        url = reverse('password_reset_confirm', kwargs={
                      'uidb64': self.uid, 'token': self.token})
        self.response = self.client.get(url, follow=True)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve(
            '/accounts/reset/{uidb64}/{token}/'.format(uidb64=self.uid, token=self.token))
        self.assertEquals(view.func.view_class, PasswordResetConfirmView)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, SetPasswordForm)

    def test_form_inputs(self):
        self.assertContains(self.response, '<input', 3)
        self.assertContains(self.response, 'type="password', 2)


class InvalidPasswordResetConfirmTests(TestCase):

    def setUp(self):
        user = User.objects.create_user(
            username='testuser',
            email='testuser@gmail.com',
            password='testpassword'
        )

        self.uid = urlsafe_base64_encode(force_bytes(user.pk))
        self.token = default_token_generator.make_token(user)

        """
        Invalidate the token by changing the password
        """

        user.set_password('nonsense')
        user.save()

        url = reverse('password_reset_confirm', kwargs={
                      'uidb64': self.uid, 'token': self.token})
        self.response = self.client.get(url, follow=True)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_html(self):
        password_reset_url = reverse('password_reset')
        self.assertContains(self.response, 'invalid password reset link')
        self.assertContains(
            self.response, 'href="{0}"'.format(password_reset_url))


class PasswordResetCompleteTests(TestCase):

    def setUp(self):
        url = reverse('password_reset_complete')
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/accounts/reset/done/')
        self.assertEquals(view.func.view_class, PasswordResetCompleteView)
