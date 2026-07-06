from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import messages
from helpermodule import studenthelper
from django.http import JsonResponse
import time
import base64
from django.conf import settings

import io 

from helpermodule import studenthelper,commonhelper
from feedback import feedbackhelper

# Create your views here.
def studentprofile(request):
    
    context = {}
    context = commonhelper.get_login_user_common_context(
        request.user, context)
  
    if request.method == 'GET':
        
        steps=request.GET.get('step','')
        
        if not steps or steps == 'step1':
           
            steps="step1"
            course_data=commonhelper.getallcourse()
            ay_data=commonhelper.getallacademicyear()
            categorydata=commonhelper.getallcategory()
            semesterdata=commonhelper.getallsemester()
            divisiondata=commonhelper.getalldivisions()
            context['course_data']=course_data
            context['ay_data']=ay_data
            context['categorydata']=categorydata
            context['semesterdata']=semesterdata
            context['divisiondata']=divisiondata

        context["step"]=steps
        
        return render(request,'student/studentprofile.html',context)
    if request.method == 'POST':
        
       
        steps=request.POST.get("step","")
        if steps=='step2':
           
            academic_data=studenthelper.get_academic_details_by_user_id(request.user.id)
            course_id=request.POST.get("course","")
            ay_year_id=request.POST.get("academic_year","")
            admission_through_id=request.POST.get("admissionthrough","")
            category_id=request.POST.get("castcategory","")
            previous_qualification=request.POST.get("txtprequalification","")
            previous_qualification_perc=request.POST.get("txtprequalificationperc","")
            roll_no=request.POST.get("txtrollno","")
            division=request.POST.get("divisions","")
            current_semester=request.POST.get("semesters","")

            user_academic_data={}
            is_academic_data_exist=False
            if academic_data:
                is_academic_data_exist=True
            user_academic_data.update({
                    "user_id":request.user.id,
                    "course_id":course_id,
                    "ay_year_id":ay_year_id,
                    "admission_through_id":admission_through_id,
                    "category_id":category_id,
                    "previous_qualification":previous_qualification,
                    "previous_qualification_perc":previous_qualification_perc,
                    "is_academic_data_exist":is_academic_data_exist,
                    "roll_no":roll_no,
                    "division":division,
                    "current_semester":current_semester

                })
            if course_id and ay_year_id and admission_through_id and category_id:
                studenthelper.save_academic_details(**user_academic_data)
        elif steps=='step3':
        
            images=""
            user_name=request.user.username
           
            if 'file_input' in request.FILES:
                    profilepic = request.FILES['file_input']
                    f_profilepic = profilepic.read()
                    images = commonhelper.uploadProfileImages(profilepic,f_profilepic,user_name)
                    print(images)
                    if images and 'image_main_url' in images and 'image_bigthumb_url' in images and 'image_smallthumb_url' in images:
                        studenthelper.updateprofileimages(images,request.user.id)
       
        elif steps=='step4':
           
            print(steps)
            family_data=studenthelper.get_family_details_by_user_id(request.user.id)
            address_data=studenthelper.get_address_details_by_user_id(request.user.id)
            fathername=request.POST.get("txtfathername","")
            mothername=request.POST.get("txtmothername","")
           
            # no_of_siblings=request.POST.get("txtsiblings","")
            # father_occupation=request.POST.get("txtfatheroccupation","")
            address1=request.POST.get("txtaddress1","")
            address2=request.POST.get("txtaddress2","")
            address3=request.POST.get("txtaddress3","")
            country=request.POST.get("country","")
            state=request.POST.get("state","")
            district=request.POST.get("district","")
            pin=request.POST.get("txtpin","")


            user_personal_data={}
            is_family_data_exist=False
            is_address_data_exist=False
            if family_data:
                is_family_data_exist=True
            if address_data:
                is_address_data_exist=True

            user_personal_data.update({
                    "user_id":request.user.id,
                    "fathername":fathername,
                    "mothername":mothername,
                    # "no_of_siblings":no_of_siblings,
                    # "father_occupation":father_occupation,
                    "address1":address1,
                    "address2":address2,
                    "address3":address3,
                    "country":country,
                    "state":state,
                    "district":district,
                    "pin":pin,
                    "is_family_data_exist":is_family_data_exist,
                    "is_address_data_exist":is_address_data_exist
                })
            if fathername and mothername:
                studenthelper.save_family_details(**user_personal_data)
            if address1 and country and state and district and pin:
                studenthelper.save_address_details(**user_personal_data)

        context["step"]=steps
        return render(request,'student/studentprofile.html',context)


def studentdashboard(request):
    context = {}
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
        return render(request,'student/studentdashboard.html',context)
    if request.method == 'POST':
        pass

def check_mobile_availability(request):
    start_time = time.time()
    res = {}
    res['success'] = False
    res['message'] = ''
    data = dict()
 
    try:
        if request.method == 'POST':
         
            mobile_data=studenthelper.is_mobile_exist(request.POST.get('mobile'))

            if mobile_data:
                res['success']=True
                res['message'] = "Mobile Number already exist"
            else:
                res['success']=False
                res['message'] = "Mobile Number not exist"
    except Exception as ex:

        res['message'] = str(ex)
    finally:
        stop_time = time.time()
        total_time = int((stop_time - start_time) * 1000)
        data = {'success': res['success'], 'timeInMillis': total_time, 'message': res['message']}
        return JsonResponse(data)   

def check_email_availability(request):
    start_time = time.time()
    res = {}
    res['success'] = False
    res['message'] = ''
    data = dict()
 
    try:
        if request.method == 'POST':
         
            mobile_data=studenthelper.is_email_exist(request.POST.get('email'))

            if mobile_data:
                res['success']=True
                res['message'] = "Email already exist"
            else:
                res['success']=False
                res['message'] = "Email Number not exist"
    except Exception as ex:

        res['message'] = str(ex)
    finally:
        stop_time = time.time()
        total_time = int((stop_time - start_time) * 1000)
        data = {'success': res['success'], 'timeInMillis': total_time, 'message': res['message']}
        return JsonResponse(data)   
    
def check_username_availability(request):
    start_time = time.time()
    res = {}
    res['success'] = False
    res['message'] = ''
    data = dict()
 
    try:
        if request.method == 'POST':
         
            mobile_data=studenthelper.is_username_exist(request.POST.get('username'))

            if mobile_data:
                res['success']=True
                res['message'] = "Username already exist"
            else:
                res['success']=False
                res['message'] = "Username not exist"
    except Exception as ex:

        res['message'] = str(ex)
    finally:
        stop_time = time.time()
        total_time = int((stop_time - start_time) * 1000)
        data = {'success': res['success'], 'timeInMillis': total_time, 'message': res['message']}
        return JsonResponse(data)   
    
def get_all_admission_through(request):
   
    start_time = time.time()
    res = {}
    res['success'] = False
    res['message'] = ''
    data = dict()
    try:
        if request.method == 'POST':
         
            admission_through_data=commonhelper.getadmisstionthrough(request.POST.get('course_id'))

            if admission_through_data:
                res['success']=True
                res['message'] = "Success"
            else:
                res['success']=False
                res['message'] = "Fail"
    except Exception as ex:

        res['message'] = str(ex)
    finally:
        stop_time = time.time()
        total_time = int((stop_time - start_time) * 1000)
        data = {'success': res['success'], 'timeInMillis': total_time, 'message': res['message'],'admission_through_data':admission_through_data}
        return JsonResponse(data)  
    


# def studentslist(request):
#     context = {}
#     context = commonhelper.get_login_user_common_context(
#         request.user, context)
#     if request.method == 'GET':
#         return render(request,'student/studentslist.html',context)
#         # return render(request,'lms/list.html',context)
#     if request.method == 'POST':
#         pass


def studentslist(request):
    
    context = {}
    user_status = commonhelper.get_login_user_common_context(request.user,context)
    course_data=commonhelper.getallcourse()
    batch_data=feedbackhelper.getallbatch()
    semester_data=commonhelper.getallsemester()
    context["course_data"]=course_data
    context["batch_data"]=batch_data
    context["semester_data"]=semester_data
    user_status=1
    if user_status == 1:
       
        inputdata = {}
        inputdata['search'] = ''
        inputdata['currentpage'] = 1
        inputdata['pagesize'] = 10

        inputdata['sort_col'] = 'au.first_name'
        inputdata['sort_dir'] = 'ASC'
        inputdata['course'] = ''
        inputdata['batch'] = ''
        inputdata['semester'] = ''

        if request.method == 'POST':
            
            if 'search' in request.POST.dict() and request.POST.get('search', '') != '':
                inputdata['search'] = request.POST.get('search', '')
            if 'currentpage' in request.POST.dict() and request.POST.get('currentpage', '') != '':
                inputdata['currentpage'] = int(request.POST.get('currentpage', 1))
            if 'sort_col' in request.POST.dict() and request.POST.get('sort_col', '') != '':
                inputdata['sort_col'] = request.POST.get('sort_col', 't1.scheduled_datetime')
            if 'sort_dir' in request.POST.dict() and request.POST.get('sort_dir', '') != '':
                inputdata['sort_dir'] = request.POST.get('sort_dir', 'DESC')
            if 'course' in request.POST.dict() and request.POST.get('course', '') != '':
                inputdata['course'] = request.POST.get('course', '')
            if 'batch' in request.POST.dict() and request.POST.get('batch', '') != '':
                inputdata['batch'] = request.POST.get('batch', '')
            if 'semester' in request.POST.dict() and request.POST.get('semester', '') != '':
                inputdata['semester'] = request.POST.get('semester', '')
            # if 'subject' in request.POST.dict() and request.POST.get('subject', '') != '':
            #     inputdata['subject'] = request.POST.get('subject', '')
            
            if 'prev_search' in request.POST and request.POST['prev_search'] != '/' and \
                    request.POST['prev_search'] != inputdata['search']:
                inputdata['currentpage'] = 1
        
            if 'prev_course' in request.POST and request.POST['prev_course'] != '/' and \
                    request.POST['prev_course'] != inputdata['course']:
                inputdata['currentpage'] = 1
            if 'prev_batch' in request.POST and request.POST['prev_batch'] != '/' and \
                    request.POST['prev_batch'] != inputdata['batch']:
                inputdata['currentpage'] = 1
            if 'prev_semester' in request.POST and request.POST['prev_semester'] != '/' and \
                    request.POST['prev_semester'] != inputdata['semester']:
                inputdata['currentpage'] = 1

    
        records = studenthelper.getallstudentslist(request, inputdata)
        context["data"] = records
        context["search"] = inputdata['search']
        context["course"] = inputdata['course']
        context["batch"] = inputdata['batch']
        context["semester"] = inputdata['semester']
       
        context = commonhelper.get_login_user_common_context(request.user, context)
        response = HttpResponse(render(request, 'student/studentslist.html', context))
        return response
    else:
        messages.add_message(request, messages.WARNING,
                             'Please login and then proceed.')
        return HttpResponseRedirect("/accounts/login")
    

def yashaswilms(request):
    context = {}
    context = commonhelper.get_login_user_common_context(
        request.user, context)
    if request.method == 'GET':
      
        return render(request,'student/Theme2.html',context)
    if request.method == 'POST':
        pass


