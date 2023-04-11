from django.contrib.auth import get_user_model
from django.urls import reverse, resolve
from django.test import TestCase

from ..forms import AnonymousCommentForm, CommentForm
from ..models import Comment, Post
from ..views import post_detail

User = get_user_model()


class PostDetailTestCase(TestCase):

    def setUp(self):
        user = User.objects.create_user(
            username='testme',
            email='testme@example.com',
            password='testmepassword'
        )

        self.published_post = Post.objects.create(
            title='published blog post',
            highlight='my highlight',
            author=user,
            body='test body',
            status='published'
        )

        self.unpublished_post = Post.objects.create(
            title='draft blog post',
            highlight='my highlight',
            author=user,
            body='test body',
        )

        self.url = self.published_post.get_absolute_url()


class PostDetailTests(PostDetailTestCase):

    def setUp(self):
        super().setUp()
        self.response = self.client.get(self.url)

    def test_published_post_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_unpublished_post_view_status_code(self):
        # A draft status post should return 404 (not found)
        response = self.client.get(self.unpublished_post.get_absolute_url())
        self.assertEquals(response.status_code, 404)

    def test_view_function(self):
        year = self.published_post.publish.year
        month = self.published_post.publish.month
        day = self.published_post.publish.day
        slug = self.published_post.slug
        view = resolve(f"/blog/{year}/{month}/{day}/{slug}/")
        self.assertEquals(view.func, post_detail)

    def test_template_used(self):
        self.assertTemplateUsed(self.response, '_base.html')
        self.assertTemplateUsed(self.response, 'blog/post/detail.html')

    def test_form_instance_for_anonymous_user(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, AnonymousCommentForm)

    def test_form_instance_for_authenticated_user(self):
        # login user
        self.client.login(
            username='testme',
            password='testmepassword',
        )
        response = self.client.get(self.url)  # generate response
        form = response.context.get('form')
        self.assertIsInstance(form, CommentForm)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_form_inputs_for_anonymous_user(self):
        # test form inputs for anonymous user
        self.assertContains(self.response, '<input', 4)
        self.assertContains(self.response, 'type="text"', 1)
        self.assertContains(self.response, 'type="email"', 1)
        self.assertContains(self.response, '<textarea', 1)

    def test_form_inputs_for_authenticated_user(self):
        # login user
        self.client.login(
            username='testme',
            password='testmepassword',
        )
        response = self.client.get(self.url)
        self.assertContains(response, '<textarea', 1)


class PostDetailCommentPostTest(PostDetailTestCase):

    def setUp(self):
        super().setUp()
        self.comment = Comment.objects.create(
            post=self.published_post,
            name='testuser01',
            email='testuser01@gmail.com',
            body='my comment'
        )
        self.response = self.client.get(self.url)

    def test_comment_details(self):
        self.assertContains(self.response, self.comment.body)
        self.assertContains(self.response, self.comment.email)


class AnonymousSuccessfulPostCommentTest(PostDetailTestCase):
    """ Check for succesful post request with AnonymousCommentForm """

    def setUp(self):
        super().setUp()
        self.response = self.client.post(self.url, {
            'name': 'testuser',
            'email': 'testuser@example.com',
            'body': 'i added a comment'
        })

    def test_redirections(self):
        self.assertRedirects(self.response, self.url)

    def test_comment_creation(self):
        self.assertTrue(Comment.objects.exists())
        self.assertEquals(self.published_post.comments.count(), 1)


class AuthenticatedSuccessfulPostCommentTest(PostDetailTestCase):
    """ Check for succesful post request with CommentForm """

    def setUp(self):
        super().setUp()
        self.response = self.client.post(self.url, {
            'name': 'testuser',
            'email': 'testuser@example.com',
            'body': 'i added a comment'
        })

    def test_redirections(self):
        self.assertRedirects(self.response, self.url)

    def test_comment_creation(self):
        self.assertTrue(Comment.objects.exists())
        self.assertEquals(self.published_post.comments.count(), 1)


class AnonymousInvalidCommentTest(PostDetailTestCase):
    """
    Check error rendering for the AnonymousCommentForm
    """

    def setUp(self):
        super().setUp()
        self.response = self.client.post(self.url, {})

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_form_error(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)


class AuthenticatedInvalidCommentTest(PostDetailTestCase):
    """
    Check error rendering for the CommentForm
    """

    def setUp(self):
        super().setUp()
        self.client.login(
            username='testme',
            password='testmepassword'
        )
        self.response = self.client.post(self.url, {})

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_form_error(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)
