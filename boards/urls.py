from django.urls import path

from .views import (
    home,
    board_topics,
    new_topic,
)

urlpatterns = [
    path('', home, name='home'),
    path('<int:pk>/', board_topics, name='board_topics'),
    path('<int:pk>/new/', new_topic, name='new_topic'),
]
