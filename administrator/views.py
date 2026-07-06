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

import pandas as pd
import numpy as np

def admindashboard(request):
    if request.method == 'GET':
        
        context = {}
        user_status = commonhelper.get_login_user_common_context(request.user,context)
        return render(request,'administrator/admindashboard.html',context)
    if request.method == 'POST':
        pass


def createuser(request):
    if request.method == 'GET':
        
        context = {}
        user_status = commonhelper.get_login_user_common_context(request.user,context)
        return render(request,'administrator/createuser.html',context)
    if request.method == 'POST':
        action=request.POST.get("action","")
      
        if action == 'upload':
                     
            my_uploaded_file = request.FILES['file_input'].read() 
            df=pd.read_excel(my_uploaded_file)
            df1 = df.replace(np.nan, '', regex=True)
            user_dict = df1.to_dict(orient='records')
           
            
            final_user_list=[]
            for item in user_dict:
                final_user_dict={}
                final_user_dict={'salutation': '',
                        'first_name': '',
                        'last_name': '',
                        'mobile_no': '',
                        'email_id': '',
                        'user_type': '',
                        'username': '',
                        'password': '',
                        'father_name': '',
                        'mother_name': '',
                        'address_line_1': '',
                        'address_line_2': '',
                        'address_line_3': '',
                        'coutry': '',
                        'state': '',
                        'district': '',
                        'pin': ''
                        }

                if item['salutation'] and item['salutation'] != None and item['salutation']!='':
                    final_user_dict['salutation']=item['salutation'].strip()
                if item['first_name'] and item['first_name'] != None and item['first_name']!='':
                    final_user_dict['first_name']=item['first_name'].strip()
                if item['last_name'] and item['last_name'] != None and item['last_name']!='':
                    final_user_dict['last_name']=item['last_name'].strip()
                if item['mobile_no'] and item['mobile_no'] != None and item['mobile_no']!='':
                    final_user_dict['mobile_no']=int(item['mobile_no'])
                if item['email_id'] and item['email_id'] != None and item['email_id']!='':
                    final_user_dict['email_id']=item['email_id'].strip()
                if item['user_type'] and item['user_type'] != None and item['user_type']!='':
                    final_user_dict['user_type']=item['user_type'].strip()
                if item['username'] and item['username'] != None and item['username']!='':
                    final_user_dict['username']=item['username'].strip()
                if item['password'] and item['password'] != None and item['password']!='':
                    final_user_dict['password']=int(item['password'])
                if item['father_name'] and item['father_name'] != None and item['father_name']!='':
                    final_user_dict['father_name']=item['father_name'].strip()
                if item['mother_name'] and item['mother_name'] != None and item['mother_name']!='':
                    final_user_dict['mother_name']=item['mother_name'].strip()
                if item['address_line_1'] and item['address_line_1'] != None and item['address_line_1']!='':
                    final_user_dict['address_line_1']=item['address_line_1'].strip()
                if item['address_line_2'] and item['address_line_2'] != None and item['address_line_2']!='':
                    final_user_dict['address_line_2']=item['address_line_2'].strip()
                if item['address_line_3'] and item['address_line_3'] != None and item['address_line_3']!='':
                    final_user_dict['address_line_3']=item['address_line_3'].strip()
                if item['coutry'] and item['coutry'] != None and item['coutry']!='':
                    final_user_dict['coutry']=item['coutry'].strip()
                if item['state'] and item['state'] != None and item['state']!='':
                    final_user_dict['state']=item['state'].strip()
                if item['district'] and item['district'] != None and item['district']!='':
                    final_user_dict['district']=item['district'].strip()
                if item['pin'] and item['pin'] != None and item['pin']!='':
                    final_user_dict['pin']=int(item['pin'])

                final_user_list.append(final_user_dict)
            

            for item in final_user_list:

                mobile_data=studenthelper.is_mobile_exist(item['mobile_no'])
                email_data=studenthelper.is_email_exist(item['email_id'])
                
                if mobile_data or email_data:
                    continue
                else:

                    user = User.objects.create_user(first_name=item['salutation']+item['first_name'],last_name=item['last_name'],email=item['email_id'],username=item['username'],password=str(item['password']))
                    user.set_password(str(item['password']))
                    user.save()
                    user_profile=User.objects.get(username=item['username'])
                    user_id=user_profile.id
                    user_data={}
                
                    user_data.update({
                        "userid":user_id,
                        "firstname":item['salutation']+item['first_name'],
                        "lastname":item['last_name'],
                        "email":item['email_id'],
                        "username":item['username'],
                        "mobile":item['mobile_no'],
                        "user_type":'s'
                    })
                    studenthelper.save_userprofile(**user_data)

                    user_personal_data={}
                    user_personal_data.update({
                        "user_id":user_id,
                        "fathername":item['father_name'],
                        "mothername":item['mother_name'],
                        "address1":item['address_line_1'],
                        "address2":item['address_line_2'],
                        "address3":item['address_line_3'],
                        "country":item['coutry'],
                        "state":item['state'],
                        "district":item['district'],
                        "pin":item['pin'],
                        "is_family_data_exist":False,
                        "is_address_data_exist":False
                    })
                    if (user_personal_data["fathername"] and user_personal_data["fathername"]!='') or (user_personal_data["mothername"] and user_personal_data["mothername"]!=''):
                        studenthelper.save_family_details(**user_personal_data)
                    if (user_personal_data['address1'] and user_personal_data["address1"]!='') or (user_personal_data['address2'] and user_personal_data["address2"]!='') or \
                        (user_personal_data['address3'] and user_personal_data["address3"]!='') or (user_personal_data['country'] and user_personal_data["country"] !='') or \
                        (user_personal_data['state'] and user_personal_data["state"] !='') or (user_personal_data['district'] and user_personal_data["district"] !='') or \
                        (user_personal_data['pin'] and user_personal_data["pin"] !='') :
                        studenthelper.save_address_details(**user_personal_data)

            return HttpResponseRedirect("/administrator/createuser")
                
               