from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
   
     path('admindashboard/', views.admindashboard,name='admindashboard'),
     path('createuser/', views.createuser,name='createuser'),
] 