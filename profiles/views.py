from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import messages

from django.contrib.auth.decorators import login_required

from helpermodule import studenthelper
from feedback import feedbackhelper
from django.template import Context
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth import authenticate, login, logout

from helpermodule import studenthelper,commonhelper
from feedback import feedbackhelper


def registration(request):
    user_roles=studenthelper.getallroles()
    context={}
    if request.method == 'GET':
        user_role=commonhelper.getallroles()
        context['user_role']=user_role
        context["flag"]=1
        
        # user_roles={"role_id":1,"role_name":"administration","role_id":2,"role_name":"faculty"}

        return render(request,'profiles/registration_new.html',context)
    if request.method == 'POST':
        
        try:
            
            txtfirstname=request.POST.get("firstname","")
            txtlastname=request.POST.get("lastname","")
            txtemail=request.POST.get("email","")
            txtusername=request.POST.get("username","")
            txtpassword=request.POST.get("password","")
            txtmobile=request.POST.get("mobile","")
            u_type=request.POST.get("user_type","")
            # user_type=''
            # if u_type=="1":
            #     user_type='s'
            # elif u_type=='2':
            #     user_type='t'
            # elif u_type=='3':
            #     user_type='e'
            # elif u_type=='4':
            #     user_type='a'
            # elif u_type=='5':
            #     user_type='ad'

            # else:
            #     user_type='s'

            user = User.objects.create_user(first_name=txtfirstname,last_name=txtlastname,email=txtemail,username=txtusername,password=txtpassword)
            user.set_password(txtpassword)
            user.save()
            user_profile=User.objects.get(username=txtusername)
            user_id=user_profile.id
            user_data={}
           
            user_data.update({
                "userid":user_id,
                "firstname":txtfirstname,
                "lastname":txtlastname,
                "email":txtemail,
                "username":txtusername,
                "mobile":txtmobile,
                "user_type":u_type
            })
            studenthelper.save_userprofile(**user_data)

            context["flag"]=2
            response = HttpResponse(render(request, 'profiles/registration.html', context))
            return response
           
        except Exception as ex:
            messages.add_message(request, messages.ERROR, str(ex))
            return HttpResponseRedirect("/registration/")
    
    return HttpResponseRedirect("/registration/")
