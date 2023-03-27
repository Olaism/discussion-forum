from django.urls import path

from .views import (
    home,
    board_topics,
    new_topic,
    topic_posts,
)

urlpatterns = [
    path('', home, name='home'),
    path('<int:pk>/', board_topics, name='board_topics'),
    path('<int:pk>/new/', new_topic, name='new_topic'),
    path('<int:pk>/topics/<int:topic_pk>/', topic_posts, name='topic_posts'),
]
