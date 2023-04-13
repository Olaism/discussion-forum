from django.db.models import Count
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, ListView

from .forms import (
    AnonymousCommentForm,
    CommentForm,
    EmailPostForm,
)
from .models import Post

from taggit.models import Tag


class PostListView(ListView):
    model = Post
    template_name = 'blog/post/list.html'
    context_object_name = 'posts'
    paginate_by = 20

    def get_queryset(self):
        tag_slug = self.kwargs.get('tag_slug', None)
        self.tag = None
        queryset = Post.published.all()
        if tag_slug:
            self.tag = get_object_or_404(Tag, slug=tag_slug)
            queryset = queryset.filter(tags__in=[self.tag])
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_post'] = Post.published.first()
        context['tag'] = self.tag
        context['most_commented_posts'] = Post.published.annotate(
            total_comments=Count('comments')).order_by('-total_comments')[:5]
        return context


def post_detail(request, slug, year, month, day):
    post = get_object_or_404(
        Post,
        slug=slug,
        status='published',
        publish__year=year,
        publish__month=month,
        publish__day=day
    )

    # get similar posts depending on the post tags id
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(
        tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags'))\
        .order_by('-same_tags', '-publish')[:4]

    # list active comments under post
    comments = post.comments.filter(active=True)

    # handle get requests
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = post
                comment.name = request.user.username
                comment.email = request.user.email
                comment.save()
                return redirect(post.get_absolute_url())
        else:
            form = AnonymousCommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = post
                comment.save()
                return redirect(post.get_absolute_url())

    else:
        if request.user.is_authenticated:
            form = CommentForm()
        else:
            form = AnonymousCommentForm()

    return render(request, 'blog/post/detail.html', {
        'post': post,
        'comments': comments,
        'similar_posts': similar_posts,
        'form': form
    })


def post_share(request, pk):
    # reference post by id
    post = get_object_or_404(Post, pk=pk)
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # form fields pass validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(
                post.title, post_url, cd['name'], cd['comment']
            )
            send_mail(subject, message, settings.EMAIL_HOST_USER, [cd['to'], ])
            sent = True

    else:
        form = EmailPostForm()

    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})
