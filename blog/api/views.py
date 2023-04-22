from django.db.models import Q
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from ..models import Comment, Post
from .serializers import (
    PostSerializer,
    CommentSerializer
)

User = get_user_model()

class PostListView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        user = get_object_or_404(User, pk=self.kwargs.get('blog_id'))
        queryset = Post.objects.filter(author__id=user.id)
        return queryset

class PostQueryView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        search_query = self.kwargs.get('search_query')
        user = get_object_or_404(User, pk=self.kwargs.get('blog_id'))
        queryset = Post.objects.filter(author__id=user.pk).filter(
            Q(title__icontains=search_query) | Q(body__icontains=search_query)
        )
        return queryset

class PostDetailView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        user_id = self.kwargs.get('blog_id')
        user = get_object_or_404(User, pk=user_id)
        queryset = Post.objects.filter(author__id=user.pk)
        return queryset

    def get_object(self, *args, **kwargs):
        queryset = self.get_queryset()
        return get_object_or_404(queryset, slug=self.kwargs.get('slug'))

class CommentListView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        user_id = self.kwargs.get('blog_id')
        post_slug = self.kwargs.get('slug')
        post = get_object_or_404(Post, slug=post_slug, author__id=user_id)
        queryset = Comment.objects.filter(post__id=post.id)
        return queryset


class CommentDetailView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        user_id = self.kwargs.get('blog_id')
        post_slug = self.kwargs.get('slug')
        user = get_object_or_404(User, pk=user_id)
        post = get_object_or_404(Post, slug=post_slug, author__id=user.id)
        queryset = Comment.objects.filter(post__id=post.id)
        return queryset

    def get_object(self, *args, **kwargs):
        queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.kwargs.get('comment_pk'))