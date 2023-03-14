from django.urls import path

from .views import (
    home,
    board_topics
)

urlpatterns = [
    path('', home, name='home'),
    path('<int:pk>/', board_topics, name='board_topics'),
]
