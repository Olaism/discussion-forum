from django.urls import path

from . import views

app_name = 'blog-api'

urlpatterns = [
    path('<int:blog_id>/posts', views.PostListView.as_view(), name='post-list'),
    path('<int:blog_id>/posts/search/<str:search_query>', views.PostQueryView.as_view(), name='post-search'),
    path('<int:blog_id>/posts/<slug:slug>', views.PostDetailView.as_view(), name='post-detail'),
    path('<int:blog_id>/posts/<slug:slug>/comments', views.CommentListView.as_view(), name='comment-list'),
    path('<int:blog_id>/posts/<slug:slug>/comments/<int:comment_pk>', views.CommentDetailView.as_view(), name='comment-detail'),
]