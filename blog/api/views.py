from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.response import Response

from ..models import Post
from .serializers import (
    BlogPostDetailSerializer,
    BlogPostEditSerializer
)

class PostDetailAPIView(generics.RetrieveDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = BlogPostDetailSerializer
    lookup_field = 'slug'

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(
            queryset,
            slug=self.kwargs.get('slug'),
            author=self.request.user
        )
        return obj

class PostEditAPIView(generics.RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = BlogPostEditSerializer
    lookup_field = 'slug'

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(
            queryset,
            slug=self.kwargs.get('slug'),
            author=self.request.user
        )
        return obj

class PostListCreateAPIView(generics.ListAPIView):
    serializer_class = BlogPostDetailSerializer

    def get_queryset(self):
        user = self.request.user
        return Post.objects.filter(author=user)

    def create(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = BlogPostEditSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)