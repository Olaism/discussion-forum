from django.urls import path

from . import views

app_name = 'blog-api'

urlpatterns = [
    path('posts/', views.PostListCreateAPIView.as_view(), name='post_list'),
    path('posts/<slug:slug>/', views.PostDetailAPIView.as_view(), name='post_detail'),
    path('posts/<slug:slug>/edit', views.PostEditAPIView.as_view(), name='post_edit'),
]