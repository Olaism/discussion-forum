from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView, ListView

from .models import Post


class PostListView(ListView):
    model = Post
    template_name = 'blog/post/list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.published.all()


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post/detail.html'
    context_object_name = 'post'

    def get_object(self):
        return get_object_or_404(
            Post,
            slug=self.kwargs.get('slug'),
            status='published',
            publish__year=self.kwargs.get('year'),
            publish__month=self.kwargs.get('month'),
            publish__day=self.kwargs.get('day')
        )
