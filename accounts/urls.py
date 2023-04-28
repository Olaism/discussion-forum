from django.urls import path

from .views import GetTokenView, UserUpdateView, signup

urlpatterns = [
    path("", UserUpdateView.as_view(), name="my_account"),
    path("signup/", signup, name="signup"),
    path("api/auth/get-token/", GetTokenView.as_view(), name="get-token"),
]
