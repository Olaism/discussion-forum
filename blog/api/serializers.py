from django.contrib.auth import get_user_model
from django.utils import timezone

from rest_framework import serializers
from taggit.serializers import (
    TagListSerializerField,
    TaggitSerializer
)

from ..models import Comment, Post

User = get_user_model()

class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class PostSerializer(TaggitSerializer, serializers.ModelSerializer):
    url = serializers.CharField(source='get_absolute_url', read_only=True)
    tags = TagListSerializerField()
    author = AuthorSerializer(read_only=True)

    def validate_publish(self, value):
        """
        Check that the publish date is not set to the past
        """
        if value < timezone.now():
            raise serializers.ValidationError("Publish date cannot be in the past")
        return value

    class Meta:
        model = Post
        fields = ('id', 'title', 'highlight', 'tags', 'author', 'body', 'url', 'publish', 'updated', 'status')
        read_only_fields = ('url', 'updated')

class PostCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('id', 'title', 'highlight', 'status')


class CommentSerializer(serializers.ModelSerializer):
    post = PostCommentSerializer()

    class Meta:
        model = Comment
        fields = ('id', 'post', 'name', 'email', 'body', 'created', 'active')
        read_only_fields = ('post', 'created', 'active')