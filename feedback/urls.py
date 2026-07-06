from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
   
     path('feedbackdashboard/', views.dashboard,name='feedbackdashboard'),
     path('academic/', views.academic,name='academic'),
     path('nonacademic/', views.nonacademic,name='nonacademic'),
     path('parent/', views.parent,name='parent'),
     path('sample/', views.sample,name='sample'),
     path('adminaddevent/', views.adminaddevent,name='adminaddevent'),
     path('addquestions/', views.addquestions,name='addquestions'),
     path('content/', views.content,name='content'),
     path('feedback_result/', views.feedback_result,name='feedback_result'),
     path('chartdata/', views.chartdata,name='chartdata'),
     path('create_feedback/', views.create_feedback,name='create_feedback'),
     path('feedbacklist/', views.feedbacklist,name='feedbacklist'),
     path('submit_feedback/', views.submit_feedback,name='academic_feedback'),
     path('add_questions_to_feedback/', views.add_questions_to_feedback,name='add_questions_to_feedback'),
     path('addscale/', views.addscale,name='addscale'),
     path('subject_allocation/', views.subject_allocation,name='subject_allocation'),
     path('subject_alloc_list/', views.subject_allocation_list,name='subject_allocation_list'),
     path('get_all_faculty_by_course_pattern_sem_div/', views.get_all_faculty_by_course_pattern_sem_div,name='get_all_faculty_by_course_pattern_sem_div'),
     path('get_faculty_by_course_pattern_sem_sub_div/', views.get_faculty_by_course_pattern_sem_sub_div,name='get_faculty_by_course_pattern_sem_sub_div'),
     path('feedback_report/', views.feedback_report,name='feedback_report'),
     path('feedback_details/', views.feedback_details,name='feedback_details'),
 
] 

