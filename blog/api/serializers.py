from django.contrib.auth import get_user_model

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
    author = AuthorSerializer()

    class Meta:
        model = Post
        fields = ('id', 'title', 'highlight', 'tags', 'author', 'body', 'url', 'publish', 'updated', 'status')
        read_only_fields = ('author', 'url', 'updated')

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