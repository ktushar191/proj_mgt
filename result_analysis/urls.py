from django.contrib import admin
from django.urls import path,include
from . import views
from django.contrib.auth import login as auth_login

urlpatterns = [
   #Student Urls
    path('add_marks/',views.result_form,name="add_marks"),
    #*******************************************************************************************
    
    #Faculty Urls
    path('faculty_dashboard/',views.faculty_dashboard,name="faculty_dashboard"),
    path('faculty_internal_marks/',views.faculty_internal_marks,name="faculty_internal_marks"),
    path('faculty_analysis/',views.faculty_analysis,name="faculty_analysis"),
    path('faculty_predictions/',views.faculty_predictions,name="faculty_predictions"),
   
]
