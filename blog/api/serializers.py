from rest_framework import serializers
from taggit.serializers import (
    TagListSerializerField,
    TaggitSerializer
)

from ..models import Post


class BlogPostDetailSerializer(serializers.ModelSerializer):

    tags = TagListSerializerField()
    author = serializers.StringRelatedField()

    class Meta:
        model = Post
        fields = ('id', 'title', 'slug', 'highlight', 
                    'tags', 'author', 'body', 'publish', 'status')

class BlogPostEditSerializer(serializers.ModelSerializer):

    tags = TagListSerializerField()

    class Meta:
        model = Post
        fields = ('title', 'highlight', 'tags', 'body', 'publish', 'status')
