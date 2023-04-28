from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import UpdateView, View

from rest_framework.authtoken.models import Token

from .forms import SignupForm

User = get_user_model()


def signup(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect("login")
    else:
        form = SignupForm()
    return render(request, "accounts/signup.html", {"form": form})

class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ("first_name", "last_name", "email")
    template_name = "accounts/my_account.html"
    success_url = reverse_lazy("my_account")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            token= Token.objects.get(user=self.request.user)
        except Token.DoesNotExist:
            token = None
        context["token"] = token
        return context

    def get_object(self):
        return self.request.user


class GetTokenView(LoginRequiredMixin, View):

    def get(self, request):
        token = Token.objects.get_or_create(user=request.user)
        return redirect('my_account')