from django.urls import path,include
from . import views
urlpatterns = [
     path('employerdashboard/', views.employerdashboard, name='employerdashboard'),
]