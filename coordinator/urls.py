from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
     path('sdcdashboard/', views.sdcdashboard,name='dashboard'),
     path('registration/', views.registration,name='registration'),
     path('temp/', views.temp,name='temp'),
     
] 
