from django.db.models import Q
from django.views.generic import ListView

from boards.models import Board, Topic, Post
from blog.models import Post as BlogPost


class SearchResultsView(ListView):
    model = Post
    template_name = 'pages/search_results.html'
    context_object_name = 'topics'

    def get_queryset(self):
        # get result by topic
        self.query = self.request.GET.get('q', '')
        queryset = Topic.objects.filter(
            Q(subject__icontains=self.query) | Q(board__name__icontains=self.query)
        )
        return queryset

    def get_context_data(self, **kwargs):
        blog_results = BlogPost.published.filter(
            Q(title__icontains=self.query) | Q(body__icontains=self.query)
        )
        context = super().get_context_data(**kwargs)
        context['query'] = self.query
        context['blog_results'] = blog_results
        return context
