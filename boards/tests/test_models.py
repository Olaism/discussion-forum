from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils.text import Truncator

from ..models import (
    Board,
    Topic,
    Post
)

from .utils import (
    create_board,
    create_post,
    create_topic
)

User = get_user_model()


class ModelsTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='ajason',
            email='ajason@gmail.com',
            password='ajasword'
        )
        self.board = create_board(
            name='my board',
            description='My board description'
        )

        # create 20 topics and assign the last topic to self.topic
        for i in range(20):
            subject = 'my subject {}'.format(i)
            self.topic = create_topic(board=self.board, subject=subject, starter=self.user)

        # create 20 posts under the last created topic and assign self.post to the last created post
        for i in range(20):
            message = f"Testing message {i}"
            self.post = create_post(topic=self.topic, message=message, author=self.user)


class BoardModelTest(ModelsTestCase):

    def test_str_representation(self):
        self.assertEqual(str(self.board), self.board.name)

    def test_get_absolute_url(self):
        self.assertEqual(self.board.get_absolute_url(), f"/boards/{self.board.pk}/")

    def test_get_posts_count(self):
        self.assertEquals(self.board.get_posts_count(), 20)

    def test_get_last_post(self):
        self.assertEquals(
            self.board.get_last_post(), 
            Post.objects.filter(topic__board=self.board).order_by('-created_at').first()
        )


class TopicModelTest(ModelsTestCase):

    def test_str_representation(self):
        truncated_subject = Truncator(self.topic.subject).chars(30)
        self.assertEqual(str(self.topic), truncated_subject)

    def test_get_absolute_url(self):
        self.assertEqual(self.topic.get_absolute_url(), f'/boards/{self.topic.board.pk}/topics/{self.topic.pk}/')

    def test_get_page_count(self):
        # get the total posts / 20
        self.assertEquals(self.topic.get_page_count(), self.topic.posts.count() / 20)

    def test_has_many_pages(self):
        self.assertEquals(self.topic.has_many_pages(), 0)

    def test_get_page_range(self):
        self.assertEqual(self.topic.get_page_range(), range(1, 2))

    def test_get_last_ten_posts(self):
        self.assertQuerysetEqual(self.topic.get_last_ten_posts(),  self.topic.posts.order_by('-created_at')[:10])


class PostModelTest(ModelsTestCase):

    def test_str_representation(self):
        truncated_msg = Truncator(self.post.message).chars(30)
        self.assertEqual(str(self.post), truncated_msg)

    def test_get_message_as_markdown(self):
        self.post.message = "# hello world"
        self.post.save()
        self.assertEqual(self.post.get_message_as_markdown(), "<h1>hello world</h1>")