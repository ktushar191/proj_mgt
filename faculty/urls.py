from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
     path('facultydashboard/', views.facultydashboard,name='facultydashboard'),
    
] 