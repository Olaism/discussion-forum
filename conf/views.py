# General requests between the board and the blog app happens here
from django.db.models import Q
from django.views.generic import ListView

from boards.models import Board, Topic, Post
from blog.models import Post as BlogPost


class SearchResultsView(ListView):
    model = Post
    template_name = 'includes/search_results.html'

    def get_queryset(self):
        self.query = self.request.GET.get('q', '')
        blog_results = BlogPost.published.filter(
            Q(title__icontains=self.query) | Q(body__icontains=self.query)
        )
        board_results = Topic.objects.filter(
            Q(subject__icontains=self.query) | Q(board__name__icontains=self.query)
        )
        results = blog_results or board_results
        return results

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.query
        return context
