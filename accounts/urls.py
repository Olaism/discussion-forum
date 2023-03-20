from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import signup

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
