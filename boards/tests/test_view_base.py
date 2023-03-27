from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class LoginRequiredBaseViewTest(TestCase):

    def test_redirection(self):
        '''
        An unauthenticated user is redirected to the login page
        '''
        login_url = reverse('login')
        response = self.client.get('/')
        self.assertEquals(response.status_code, 302)


class BaseTestView(TestCase):

    def test_url_redirect_to_home_view(self):
        '''
        An authenticated user is redirected to the homepage
        '''
        User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )
        self.client.login(
            username='testuser',
            password='testpassword'
        )
        home_url = reverse('home')
        response = self.client.get('/')
        self.assertRedirects(response, home_url)
