from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Post, Comment

User = get_user_model()


class CommentModelTest(TestCase):

    def setUp(self):
        user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )
        post = Post.objects.create(
            title='post title',
            highlight='post highlight',
            author=user,
            body='post body',
            status='published'
        )
        self.comment = Comment.objects.create(
            post=post,
            name='commentator',
            email='testmail@example.com',
            body='comment body',
        )

    def test_str_representation(self):
        self.assertEquals(str(self.comment), f"comment by {self.comment.name} on {self.comment.created}")
