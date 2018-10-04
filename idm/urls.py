from django.urls import path
from . import views
from . import face_rec
from django.contrib.auth import login, logout

urlpatterns = [
    path('index/', views.home, name='root'),
    path('', views.home, name='home'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('partial/', views.partial_login, name='partial-signin'),
    path('user/<int:pk>/update/', views.UpdateUserFace.as_view(), name='update-user'),
    path('user/<int:pk>/verify/', views.VerifyUserFace.as_view(), name='verify-face'),
    path('user/<int:pk>/sucess/', views.success_view, name='success'),
    path('user/<int:pk>/error/', views.error_view, name='error'),
    path('api/users/', views.UsersList.as_view(), name='users'),
    path('api/users/<int:pk>/', views.UsersDetail.as_view(), name='user-detail'),
    path('api/products/', views.ProductList.as_view(), name='users'),
    path('api/products/<int:pk>/',
         views.ProductDetail.as_view(), name='user-detail'),
    path('users/all/', views.view_users, name='all-users'),
    path('products/', views.view_product, name='products'),
    path('user-logs/', views.view_logs, name='logs'),

    path('recognize/', face_rec.recognize),
    path('train/', face_rec.train),
    path('new/', face_rec.new),
    path('users/', face_rec.users),

    path('login/', views.my_login_view, name='login'),
    path('logout/', logout, name='logout'),
]
