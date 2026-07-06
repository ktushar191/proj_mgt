from django.urls import path,include
from . import views
urlpatterns = [
     path('alumnidashboard/', views.alumnidashboard,name='alumnidashboard'),
]