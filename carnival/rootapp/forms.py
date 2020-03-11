from django import forms

from .models import Setcamera,Users
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']



class UsersForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ("__all__")


class SetcameraForm(forms.ModelForm):
    class Meta:
        model = Setcamera
        fields = ("__all__")
