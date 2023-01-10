from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.LoginPage, name="login"),
    path("logout/", views.LogoutUser, name="logout"),
    path("register/", views.registerPage, name="register"),
    path('', views.home, name="home"),
    path("room/<str:pk>/", views.room, name="room"),
    path("profile/<str:pk>/", views.userProfile, name="user_profile"),
    path('createroom/', views.CreateRoom, name="create_room"),
    path('updateroom/<str:pk>/', views.UpdateRoom, name="update_room"),
    path('deleteroom/<str:pk>/', views.DeleteRoom, name="delete_room"),
    path('deletemessage/<str:pk>/', views.DeleteMessage, name="delete_msg"),
]