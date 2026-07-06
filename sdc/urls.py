from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
     path('addproject', views.addproject,name='addproject'),
     path('projectallocation/', views.projectallocation,name='projectallocation'),
     path('documentupload/', views.documentupload,name='documentupload'),
     path('projectdetails/', views.projectdetails,name='projectdetails'),
] 