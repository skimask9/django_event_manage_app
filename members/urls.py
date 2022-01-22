from django.contrib import admin
from django.urls import path
from django.urls import include
from . import views

urlpatterns = [
    path('login_user', views.login_user, name = "login"),
    path('logout_user', views.logout_user, name = "logout"),
    path('register_user', views.register_user, name = "register-user"),
]
