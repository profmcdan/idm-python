from django.contrib.auth.models import AbstractUser, User
from django.db import models
from django.urls import reverse


class Profile(models.Model):
    # First/last name is not a global-friendly pattern
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(blank=True, max_length=255, null=True)
    residence = models.CharField(max_length=50, null=True)
    country = models.CharField(max_length=50, null=True)
    education = models.CharField(max_length=150, null=True)
    occupation = models.CharField(max_length=150, null=True)
    marital_status = models.CharField(max_length=50, null=True)
    bio = models.TextField(null=True)
    profile_face = models.FileField(upload_to='profile/', null=True)
    face = models.FileField(upload_to='myface/',
                            null=True, verbose_name='Upload Face')
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email

    def get_update_url(self):
        return reverse('update-user', kwargs={'pk': self.pk})

    def get_verify_url(self):
        return reverse('verify-face', kwargs={'pk': self.pk})

    def get_login_success_url(self):
        return reverse('success', kwargs={'pk': self.pk})

    def get_login_error_url(self):
        return reverse('error', kwargs={'pk': self.pk})


class Face(models.Model):
    userr = models.ForeignKey(
        Profile, on_delete=models.DO_NOTHING, null=True, related_name='usr')
    pic = models.FileField(upload_to='faces/')


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='Name', null=True)
    description = models.CharField(max_length=255, null=True)
    owner = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class UserLogHistory(models.Model):
    user = models.CharField(max_length=255)
    attempt = models.CharField(max_length=255, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{0} - {1}'.format(self.user, self.attempt)
