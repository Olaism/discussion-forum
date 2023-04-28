from django.urls import path

from . import views

app_name = 'blog-api'

urlpatterns = [
    path('posts', views.AllPostView.as_view(), name='all_posts'),
    path('self/posts/', views.SelfPostView.as_view(), name='my_posts'),
    path('posts/search/<str:search_query>', views.PostQueryView.as_view(), name='post-search'),
    path('users/<int:blog_id>/posts', views.PostListByUserView.as_view(), name='post-list-by-user'),
    path('<int:blog_id>/posts/<slug:slug>', views.PostDetailByUserView.as_view(), name='post-detail-by-user'),
    path('<int:blog_id>/posts/<slug:slug>/comments', views.CommentListByUserPostView.as_view(), name='comment-list-by-user'),
    path('<int:blog_id>/posts/<slug:slug>/comments/<int:comment_pk>', views.CommentDetailByUserPostView.as_view(), name='comment-detail-by-user'),
]