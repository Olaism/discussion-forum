from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class SignupForm(UserCreationForm):
    email = forms.CharField(
        max_length=254,
        required=True,
        widget=forms.EmailInput()
    )

    class Meta:
        model = User
        fields = ('username', 'email')
