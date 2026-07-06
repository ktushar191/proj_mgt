from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
     path('courses/', views.courses,name='courses'),
     path('subject/', views.subject,name='subject'),
     path('mca/', views.mca,name='mca'),
     path('mba/', views.mba,name='mba'),
     path('create_test/', views.create_test,name='mba'),
     path('nextpage/', views.nextpage,name='mba'),
     path('mcqexam/', views.mcqexam,name='mcqexam'),
     path('mcqdashboard/', views.mcqdashboard,name='mcqexam'),
     path('createmcq/', views.createmcq,name='createmcq'),
     path('get_all_subjects_by_course_and_sem/', views.get_all_subjects_by_course_and_sem,name='get_all_subjects_by_course_and_sem'),
     path('mcqlist/', views.mcqlist,name='mcqlist'),
     path('addmcqquestions/', views.addmcqquestions,name='addmcqquestions'),
     path('mcqresult/', views.mcqresult,name='mcqresult'),
     path('add_questions_to_mcq/', views.add_questions_to_mcq,name='add_questions_to_mcq'),
     path('get_all_subjects_by_course_sem_pattern/', views.get_all_subjects_by_course_sem_pattern,name='get_all_subjects_by_course_sem_pattern'),
     path('mcqexamlist/', views.mcqexamlist,name='mcqexamlist'),
     path('mcqallresult/', views.mcqallresult,name='mcqallresult'),

] 
