from django.urls import reverse_lazy
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
import numpy as np
import urllib
import requests
import json
import cv2
import os
from PIL import Image
from io import BytesIO
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Product, Face, UserLogHistory, Profile
from .forms import FaceForm
from .serializer import ProductSerializer, UserSerializer

from .forms import CustomUserCreationForm
from .face_api import recognize_face, train_faces
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.core.files.base import ContentFile
from skimage import io
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


# define the path to the face detector
FACE_DETECTOR_PATH = "{base_path}/cascades/haarcascade_frontalface_default.xml".format(
    base_path=os.path.abspath(os.path.dirname(__file__)))

server = 'http://127.0.0.1:8000'

# METHOD #1: OpenCV, NumPy, and urllib


def url_to_image(url):
    # download the image, convert it to a NumPy array, and then read
    # it into OpenCV format
    image = io.imread(url)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # return the image
    return image


@login_required
def view_users(request):
    template_name = 'users.html'
    data = Profile.objects.all()
    return render(request, template_name, {'users': data})


@login_required
def view_product(request):
    template_name = 'product.html'
    data = None
    return render(request, template_name, {'users': data})


def my_login_view(request):
    template_name = 'registration/login.html'
    form = AuthenticationForm(request.POST or None)
    if form.is_valid():
        username = request.POST['username']
        password = request.POST['password']
        if username and password:
            user = authenticate(request, username=username, password=password)
            print('I got here')
            if user is not None:
                userLog = UserLogHistory(user=username, attempt='success')
                userLog.save()
                print(userLog)
                login(request, user)
                profile = Profile.objects.get(user=user)
                print(profile)
                # Redirect to a success page.
                return redirect(profile.get_verify_url())
            else:
                userLog = UserLogHistory(user=username, attempt='failed')
                userLog.save()
    return render(request, template_name, {'form': form})


def home(request):
    template_name = 'index.html'
    data = {}
    return render(request, template_name, data)


class UsersList(ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = UserSerializer


class UsersDetail(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProductList(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetail(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('update-user')
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        usr = form.save()
        key = usr.pk
        usr = get_object_or_404(User, pk=key)
        profile = Profile(user=usr)
        profile.save()
        print(usr)
        return redirect(profile.get_update_url())


class UpdateUserFace(generic.UpdateView):
    model = Profile
    fields = ['name', 'residence', 'country',
              'education', 'occupation', 'bio', 'profile_face', ]
    success_url = reverse_lazy('root')
    template_name = 'registration/update.html'

    def form_valid(self, form):
        usr = form.save()
        key = usr.pk
        usr = get_object_or_404(Profile, pk=key)
        face = Face(userr=usr)
        face.save()
        face_copy = ContentFile(usr.profile_face.read())
        face_copy_name = usr.profile_face.name.split("/")[-1]
        face.pic.save(face_copy_name, face_copy)
        face.save()
        usr.face = None
        usr.save()
        training_result = train_faces()
        print(training_result)
        return redirect(self.get_success_url())


class VerifyUserFace(generic.UpdateView):
    model = Profile
    fields = ['face', ]
    success_url = reverse_lazy('root')
    template_name = 'registration/verify.html'

    def form_valid(self, form):
        usr = form.save()
        key = usr.pk
        usr = get_object_or_404(Profile, pk=key)
        usr_face = usr.face
        face_url = server + usr_face.url
        face_image = url_to_image(face_url)
        user_face = recognize_face(face_image)
        print(user_face)
        if user_face == usr.pk:
            usr.is_verified = True
            usr.face = None
            usr.save()
            userLog = UserLogHistory(
                user=self.request.user.username, attempt='success')
            userLog.save()
            print(userLog)
            return redirect(usr.get_login_success_url())
        else:
            usr.is_verified = False
            usr.face = None
            usr.save()
            userLog = UserLogHistory(
                user=self.request.user.username, attempt='failed')
            userLog.save()
            return redirect(usr.get_login_error_url())


def error_view(request, pk):
    usr = get_object_or_404(Profile, pk=pk)
    template_name = 'registration/error.html'
    data = {'usr': usr}
    return render(request, template_name, data)


def success_view(request, pk):
    usr = get_object_or_404(Profile, pk=pk)
    template_name = 'registration/success.html'
    data = {'usr': usr}
    return render(request, template_name, data)


@login_required
def partial_login(request):
    template_name = 'registration/partial.html'
    loggedUser = request.user
    profile = Profile.objects.get(user=loggedUser)
    data = {'profile': profile}
    return render(request, template_name, data)


@login_required
def view_logs(request):
    template_name = 'logs.html'
    logs = UserLogHistory.objects.all()
    return render(request, template_name, {'userLogs': logs})
