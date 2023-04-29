from django.db.models import Q
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from .mixins import CustomCreateModelMixin
from ..models import Comment, Post
from .serializers import (
    PostSerializer,
    CommentSerializer
)
from .utils import get_user

User = get_user_model()

class AllPostView(generics.ListAPIView):
    """ returns all published posts from all authors """
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,]

    def get_queryset(self):
        queryset = Post.published.all()
        return queryset

class SelfPostView(generics.ListCreateAPIView):
    """ return all posts for an authenticated user """
    # authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated,]
    serializer_class = PostSerializer

    def get_queryset(self):
        instance = self
        user = get_user(instance)
        queryset = Post.objects.filter(author=user)
        return queryset

    def perform_create(self, serializer):
        user = get_user(self)
        serializer.save(author=user)

class PostListByUserView(generics.ListAPIView):
    """ returns all published posts from a user of specific id """
    serializer_class = PostSerializer
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        user = get_object_or_404(User, pk=self.kwargs.get('blog_id'))
        queryset = Post.published.filter(author__id=user.id)
        return queryset

class PostQueryView(generics.ListAPIView):
    """ returns all published posts that match a specific query """
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        search_query = self.kwargs.get('search_query')
        # user = get_object_or_404(User, pk=self.kwargs.get('blog_id'))
        queryset = Post.published.filter(
            Q(title__icontains=search_query) | Q(body__icontains=search_query)
        )
        return queryset

class PostDetailByUserView(generics.RetrieveAPIView):
    """ returns a detail info of a post """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        user_id = self.kwargs.get('blog_id')
        user = get_object_or_404(User, pk=user_id)
        queryset = Post.published.filter(author__pk=user.pk)
        return queryset

    def get_object(self, *args, **kwargs):
        queryset = self.get_queryset()
        return get_object_or_404(queryset, slug=self.kwargs.get('slug'))

class SelfPostDetailView(generics.RetrieveUpdateDestroyAPIView):
    """ returns a detail info of an authenticated user """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        instance = self
        user = get_user(instance)
        queryset = Post.objects.filter(author__id=user.pk)
        return queryset

    def get_object(self, *args, **kwargs):
        queryset = self.get_queryset()
        return get_object_or_404(queryset, slug=self.kwargs.get('slug'))

class CommentListByUserPostView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        user_id = self.kwargs.get('blog_id')
        post_slug = self.kwargs.get('slug')
        post = get_object_or_404(Post, slug=post_slug, author__id=user_id, status='published')
        queryset = Comment.objects.filter(post__id=post.id)
        return queryset

    def perform_create(self, serializer):
        instance = self
        user = get_user(instance)
        post = get_object_or_404(Post, slug=self.kwargs.get('slug'))
        serializer.save(name=user.username, email=user.email, post=post)


class CommentDetailByUserPostView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        user_id = self.kwargs.get('blog_id')
        post_slug = self.kwargs.get('slug')
        user = get_object_or_404(User, pk=user_id)
        post = get_object_or_404(Post, slug=post_slug, author__id=user.id, status='published')
        queryset = Comment.objects.filter(post__id=post.id, active=True)
        return queryset

    def get_object(self, *args, **kwargs):
        queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.kwargs.get('comment_pk'), active=True)