from django.urls import path

from .views import (
    BoardListView,
    TopicListView,
    new_topic,
    PostEditView,
    PostListView,
    reply_topic,
)

urlpatterns = [
    path('', BoardListView.as_view(), name='home'),
    path('<int:pk>/', TopicListView.as_view(), name='board_topics'),
    path('<int:pk>/new/', new_topic, name='new_topic'),
    path('<int:pk>/topics/<int:topic_pk>/',
         PostListView.as_view(), name='topic_posts'),
    path('<int:pk>/topics/<int:topic_pk>/reply/',
         reply_topic, name='reply_topic'),
    path('<int:pk>/topics/<int:topic_pk>/posts/<int:post_pk>/edit/',
         PostEditView.as_view(), name='edit_post'),
]
