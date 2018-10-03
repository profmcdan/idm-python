from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Profile
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = UserChangeForm.Meta.fields


class FaceForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['face', ]
