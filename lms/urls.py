from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
 path('addcontent/', views.addcontent,name='content'),
  path('lmsdashboard/', views.lmsdashboard,name='lmsdashboard'),
     path('lms_studycontent/', views.lms_studycontent,name='lms_studycontent'),
     path('lms_notes/', views.notes,name='lms_notes'),
     path('lms_PYQ/', views.PYQ,name='lms_PYQ'),
     path('lms_other/', views.other,name='lms_other'),
     path('lmscertificate/', views.lmscertificate,name='lmscertificate'),
     path('lmsaptitude/', views.lmsaptitude,name='lmsaptitude'),
     path('lms_syllabus/', views.lmssyllabus,name='lms_syllabus'),
     path('addsubjects/', views.addsubjects,name='addsubjects'),
     path('lms_library/', views.lms_library,name='lms_library'),
     path('lms_project/', views.lms_project,name='lms_project'),
     
] 

