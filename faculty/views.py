from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from helpermodule import studenthelper,commonhelper
from django.template import Context
from .models import *
from django.contrib.auth import authenticate, login, logout
from feedback import feedbackhelper

# Create your views here.
def facultydashboard(request):
    context={}
    context = commonhelper.get_login_user_common_context(
        request.user, context)
    
    if request.method == 'GET':
        audience_id=""
        if context['user_profile'][0]['user_type']=='s':
            audience_id=1
        elif context['user_profile'][0]['user_type']=='f':
             audience_id=2
        elif context['user_profile'][0]['user_type']=='a':
             audience_id=2
        elif context['user_profile'][0]['user_type']=='e':
             audience_id=3
        elif context['user_profile'][0]['user_type']=='al':
             audience_id=4
        feedback_data=None
        feedback_data=studenthelper.getfeedbackdata(audience_id)
        context['feedback_data']=feedback_data
    user_status = commonhelper.get_login_user_common_context(request.user,context)
    if request.method == 'GET':
        return render(request,'faculty/facultydashboard.html',context)
    if request.method == 'POST':
        pass