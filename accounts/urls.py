from django.contrib import admin
from django.urls import path,include
from . import views
from django.contrib.auth import login as auth_login

urlpatterns = [
     path('', views.userlogin,name='userlogin'),
     path('Logout', views.Logout,name='Logout')
     
] 