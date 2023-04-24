from django.contrib.syndication.views import Feed
from django.urls import reverse_lazy

from .models import Post


class LatestPostsFeed(Feed):
    title = 'Django Blog'
    link = reverse_lazy('blog:post_list')
    description = 'New posts from the django blog'

    def items(self):
        return Post.published.all()[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.highlight

    def item_pubdate(self, item):
        return item.publish