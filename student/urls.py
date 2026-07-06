from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
     path('studentprofile/', views.studentprofile,name='studentprofile'),
     path('studentdashboard/', views.studentdashboard,name='dashboard'),
     path('check_mobile_availability/', views.check_mobile_availability,name='check_mobile_availability'),
     path('check_email_availability/', views.check_email_availability,name='check_email_availability'),
     path('check_username_availability/', views.check_username_availability,name='check_username_availability'),
     path('get_all_admission_through/', views.get_all_admission_through,name='get_all_admission_through'),
     path('studentslist/', views.studentslist,name='studentslist'),
     path('yashaswilms/', views.yashaswilms,name='studentslist'),
     
   
] 
