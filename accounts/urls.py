from django.urls import path

from .views import UserUpdateView, signup

urlpatterns = [
    path("", UserUpdateView.as_view(), name="my_account"),
    path("signup/", signup, name="signup"),
]
