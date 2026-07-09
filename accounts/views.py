from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import messages

from django.contrib.auth.decorators import login_required

from helpermodule import studenthelper,commonhelper
from django.template import Context

from .models import *
from django.contrib.auth import authenticate, login, logout

from feedback import feedbackhelper
import traceback

def userlogin(request):
    return render(request, "accounts/test.html")

# def userlogin(request):
#     context={}
#     # user_status = commonhelper.get_login_user_common_context(request.user,context)
#     if request.method == 'GET':
#         return render(request,'accounts/login.html',{})
#     if request.method == 'POST':
#         try:
            
#             txtusername=request.POST['txtusername']
#             txtpassword=request.POST['txtpassword']
#             user = authenticate(username=txtusername, password=txtpassword)
#             if user is not None:
#                 login(request,user)
#                 commonhelper.add_session_log(request, 'password')
#                 context = {}
#                 context = commonhelper.get_login_user_common_context(
#                     user, context)
                
#                 if(context['user_profile'][0]['user_type']=='s'):
#                     return HttpResponseRedirect("/student/studentdashboard/")
#                 elif(context['user_profile'][0]['user_type']== 'a'):
#                     return HttpResponseRedirect("/administrator/admindashboard/")
#                 elif(context['user_profile'][0]['user_type']=='f'):
#                     return HttpResponseRedirect("/faculty/facultydashboard/")
#                 elif(context['user_profile'][0]['user_type']=='c'):
#                     return HttpResponseRedirect("/coordinator/sdcdashboard/")
#                 elif(context['user_profile'][0]['user_type']=='e'):
#                     return HttpResponseRedirect("/employer/employerdashboard/")
#                 elif(context['user_profile'][0]['user_type']=='al'):
#                     return HttpResponseRedirect("/alumni/alumnidashboard/")
#             else:
#                 messages.add_message(request, messages.ERROR,
#                                          'The username & password you entered did not match our records. '
#                                          'Please try again.')
#                 return HttpResponse(render(request, 'accounts/login.html', context))
                
#         except Exception as ex:
#             messages.add_message(request, messages.ERROR, str(ex))
#             return HttpResponse("<pre>" + traceback.format_exc() + "</pre>",status=500)
#             # return HttpResponse(render(request, 'accounts/login1.html', context))
#     return HttpResponse(render(request, 'accounts/login.html', context))



def Logout(request):
    logout(request)
    return redirect('/')