from django.test import SimpleTestCase

from ..forms import (
    AnonymousCommentForm,
    CommentForm,
    EmailPostForm,
)


class AnonymousCommentFormTest(SimpleTestCase):

    def test_form_fields(self):
        form = AnonymousCommentForm()
        expected = ['name', 'email', 'body']
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)


class CommentFormTest(SimpleTestCase):

    def test_form_fields(self):
        form = CommentForm()
        expected = ['body']
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)


class EmailPostFormTest(SimpleTestCase):

    def test_form_fields(self):
        form = EmailPostForm()
        expected = ['name', 'email', 'to', 'comment']
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)
