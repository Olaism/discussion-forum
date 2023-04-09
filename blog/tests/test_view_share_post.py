from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase
from django.urls import reverse, resolve

from ..models import Post
from ..forms import EmailPostForm
from ..views import post_share

User = get_user_model()


class PostShareViewTestCase(TestCase):

    def setUp(self):
        # create an author
        user = User.objects.create_user(
            username='testuser',
            email='testemail@gmail.com',
            password='testpassword'
        )
        # Create a published post
        self.post = Post.objects.create(
            title='an example post',
            highlight='a post highlight',
            author=user,
            body='post body',
            status='published'
        )
        # get the post url
        self.url = reverse('blog:post_share', kwargs={'pk': self.post.pk})


class PostShareViewTest(PostShareViewTestCase):

    def setUp(self):
        super().setUp()
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve(f"/blog/{self.post.pk}/share/")
        self.assertEquals(view.func, post_share)

    def test_has_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, EmailPostForm)

    def test_csrf_token(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_inputs(self):
        self.assertContains(self.response, '<input',  5)  # The search and hidden(csrf) input makes it five
        self.assertContains(self.response, 'type="text"', 1)
        self.assertContains(self.response, 'type="email"', 2)
        self.assertContains(self.response, '<textarea', 1)


class SuccessfulPostShareViewTest(PostShareViewTestCase):
    def setUp(self):
        super().setUp()
        self.response = self.client.post(self.url, data={
            'name': 'testuser',
            'email': 'testuser@example.com',
            'to': 'fiver@example.com',
            'comment': 'some comment'
        })
        self.email = mail.outbox[0]

    def test_successful_message(self):
        self.assertContains(self.response, 'Post sent successfully')

    def test_sent_update(self):
        sent = self.response.context.get('sent')
        self.assertTrue(sent)

    def test_message_sent(self):
        pass

    def test_email_subject(self):
        subject = '{} ({}) recommends you reading "{}"'.format('testuser', 'testuser@example.com', self.post.title)
        self.assertEqual(subject, self.email.subject)

    def test_email_message(self):
        request = self.response.wsgi_request
        post_url = request.build_absolute_uri(self.post.get_absolute_url())
        message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(
            self.post.title, post_url, 'testuser', 'some comment'
        )
        self.assertIn(message, self.email.body)
        self.assertIn("testuser", self.email.body)

    def test_email_to(self):
        self.assertEqual(["fiver@example.com", ], self.email.to)


class InvalidPostShareViewTest(PostShareViewTestCase):
    def setUp(self):
        super().setUp()
        self.response = self.client.post(self.url, {})

    def test_status_code(self):
        # invalid form input redirects to the same page
        self.assertEqual(self.response.status_code, 200)

    def test_form_error(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)
