from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import Face, UserLogHistory, Profile


# class CustomUserAdmin(UserAdmin):
#     add_form = CustomUserCreationForm
#     form = CustomUserChangeForm
#     model = Profile
#     list_display = ['email', 'username', 'name']


admin.site.register(Profile)
admin.site.register(Face)
admin.site.register(UserLogHistory)
