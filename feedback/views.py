from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import messages
from feedback import feedbackhelper
from mcqexams import mcqhelper
import matplotlib.pyplot as plt
import numpy as np
from django.http import JsonResponse
import time
from django.conf import settings
from helpermodule import studenthelper,commonhelper
from datetime import datetime
import pandas as pd
import json
# Create your views here.
  

def dashboard(request):
    context = {}
    context = commonhelper.get_login_user_common_context(request.user, context)
    if request.method =="GET":
        return render(request,'feedback/feedbackdashboard.html',context)
    if request.method == 'POST':
        pass

def academic(request):
    context = {}
    context = commonhelper.get_login_user_common_context(request.user, context)
    if request.method =="GET":
        return render(request,'feedback/academic.html',context)
    if request.method == 'POST':
        pass

def nonacademic(request):
    context = {}
    context = commonhelper.get_login_user_common_context(request.user, context)
    if request.method =="GET":
        return render(request,'feedback/nonacademic.html',context)
    if request.method == 'POST':
        pass

def parent(request):
    context = {}
    context = commonhelper.get_login_user_common_context(request.user, context)
    if request.method =="GET":
        return render(request,'feedback/parent.html',context)
    if request.method == 'POST':
        pass

def sample(request):
    context = {}
    context = commonhelper.get_login_user_common_context(request.user, context)
    if request.method =="GET":
        return render(request,'feedback/sample.html',context)
    if request.method == 'POST':
        pass

def adminaddevent(request):
    context = {}
    context = commonhelper.get_login_user_common_context(request.user, context)
    if request.method =="GET":
        return render(request,'feedback/adminaddevent.html',context)
    if request.method == 'POST':
        pass

def addquestions(request):
    context = {}
    context = commonhelper.get_login_user_common_context(request.user, context)
  
    if request.method =="GET":
        scale_dict=feedbackhelper.get_all_scales()
        feedback_type_dict=feedbackhelper.getallfeedbacktypes()
        audience=feedbackhelper.getallaudience()
        context['scale_dict']=scale_dict
        context['feedback_type_dict']=feedback_type_dict
        context['audience']=audience
        return render(request,'feedback/addfeedbackquestions.html',context)
    if request.method == 'POST':
        action=request.POST.get("action_event","")
        feedback_question_dict={}
        questions_dict_to_save={}
        feedback_questions_list=[]
        

        now = datetime.now()
        now.strftime('%m/%d/%Y')
        user_id=request.user.id
        if action == 'add':
            feedback_type_id=request.POST.get("feedback_type","")
            scale_id=request.POST.get("scale","")
            question=request.POST.get("txt_feedback_question","")
            audience_id=request.POST.get("audience","")
           
            user_id=request.user.id

            feedback_question_dict.update({
                "feedback_type_id":feedback_type_id,
                "question":question,
                "scale_id":scale_id,
                "audience_id":audience_id})
            feedback_questions_list.append(feedback_question_dict)
            
        if action == 'upload':
         
           my_uploaded_file = request.FILES['file_input'].read() 
           import pandas as pd
           df=pd.read_excel(my_uploaded_file)
           df1=df[['question', 'feedback_type_id',
                        'scale_id', 'audience_id']]
           df1.dropna(subset=['question'], inplace=True)
                        
           feedback_questions_list=df1.to_dict(orient='records')
           
        questions_dict_to_save.update({
        
            "feedback_question_list": feedback_questions_list,
            "current_datetime":now,
            "user_id":user_id
        })

        feedbackhelper.savefeedbackquestion(**questions_dict_to_save)

    return HttpResponseRedirect("/feedback/addquestions")


def content(request):
    context = {}
    context = commonhelper.get_login_user_common_context(request.user, context)
    if request.method == 'GET':
        
        course_data=feedbackhelper.getallcourse()
        ay_data=feedbackhelper.getallacademicyear()
        semester_data=feedbackhelper.getallsemester()
        subject_data=feedbackhelper.getallsubjects()
        
        return render(request, 'lms/content.html',context)
    if request.method == 'POST':
        txtcourseid = request.POST.get("course", "")
        txtay_id = request.POST.get("academic_year", "")
        txtsem_id = request.POST.get("Semester", "")
        txtsub_id = request.POST.get("subject", "")
        txttitle = request.POST.get("title", "")
        txttopic = request.POST.get("topic", "")
        txttype_id = request.POST.get("type_id", "")
        txtcontent = request.POST.get("content", "")
        txtlink = request.POST.get("link", "")
        content_data = {}

        content_data.update({
            "course": txtcourseid,
            "academic_year": txtay_id,
            "Semester": txtsem_id,
            "subject": txtsub_id,
            "title": txttitle,
            "topic": txttopic,
            "type_id": txttype_id,
            "content": txtcontent,
            "link": txtlink,

        })
        feedbackhelper.save_content(**content_data)



def feedback_result(request):
    context = {}
    context = commonhelper.get_login_user_common_context(
        request.user, context)
    if request.method =="GET":
        
        data={}
        student_dict={}
        teacher_dict={}
        employer_dict={}
        alumni_dict={}
        feedback_result=commonhelper.getallfeedbackresults()
        feedback_result_count=commonhelper.getallfeedbackresultscount()
        s_dict={}
        t_dict={}
        e_dict={}
        a_dict={}
        for item in feedback_result:
            
            chartdata=[]
            chartdata.append(item['strongly_agree'])
            chartdata.append(item['agree'])
            chartdata.append(item['neutral'])
            chartdata.append(item['disagree'])
            chartdata.append(item['strongly_disagree'])
            

            labels = [ 
            'Strongly Agree', 
            'Agree',  
            'Neutral',  
            'Disagree',  
            'Strongly Disagree',  
            ] 
            if item['type']=='s':
               s_dict.update({item['question_id']:{'labels':labels,'chartLabel':item['question'],'chartdata':chartdata}})
            if item['type']=='t':
               t_dict.update({item['question_id']:{'labels':labels,'chartLabel':item['question'],'chartdata':chartdata}})
            if item['type']=='e':
               e_dict.update({item['question_id']:{'labels':labels,'chartLabel':item['question'],'chartdata':chartdata}})
            if item['type']=='a':
               a_dict.update({item['question_id']:{'labels':labels,'chartLabel':item['question'],'chartdata':chartdata}})
            
        student_dict.update({'student':s_dict})
        teacher_dict.update({'teacher':t_dict})
        employer_dict.update({'employer':e_dict})
        alumni_dict.update({'alumni':a_dict})
        data.update(student_dict)
        data.update(teacher_dict)
        data.update(employer_dict)
        data.update(alumni_dict)
        context['data']=data
        return render(request,'feedback/feedback_result.html',context)
    if request.method == 'POST':
        pass


def chartdata(request):
    start_time = time.time()
    res = {}
    res['success'] = False
    res['message'] = ''
    data = dict()
 
    try:
        if request.method == 'POST':

          
            student_dict={}
            teacher_dict={}
            employer_dict={}
            alumni_dict={}

            
            labels = [ 
            'Strongly Agree', 
            'Agree',  
            'Neutral',  
            'Disagree',  
            'Strongly Disagree',  
            ] 
            chartLabel = "Student"
            chartdata = [10, 20, 30, 25, 20] 
            data ={ 
                        "labels":labels, 
                        "chartLabel":chartLabel, 
                        "chartdata":chartdata, 
                } 

            if data:
                res['success']=True
               
            else:
                res['success']=False
                
    except Exception as ex:

        res['message'] = str(ex)
    finally:
        stop_time = time.time()
        total_time = int((stop_time - start_time) * 1000)
        data = {'success': res['success'], 'timeInMillis': total_time, 'data': data}
        return JsonResponse(data) 


def create_feedback(request):
    context = {}
    context = commonhelper.get_login_user_common_context(
        request.user, context)
    if request.method =="GET":
        feedback_types=feedbackhelper.getallfeedbacktypes()
        academic_years=feedbackhelper.getallacademicyear()
        audience=feedbackhelper.getallaudience()
        context['feedback_types']=feedback_types
        context['academic_years']=academic_years
        context['audience']=audience

        return render(request,'feedback/create_feedback.html',context)
    if request.method == 'POST':
        
        feedback_type=request.POST.get('feedback_type','')
        feedback_name=request.POST.get('feedback_name','')
        academic_year=request.POST.get('academic_year','')
        audience=request.POST.get('audience','')
        start_date=request.POST.get('start_date','')
        start_time=request.POST.get('start_time','')
        end_date=request.POST.get('end_date','')
        end_time=request.POST.get('end_time','')

        now = datetime.now()
        now.strftime('%m/%d/%Y')

        feedback_data={}
        if feedback_type=='':
            feedback_type=0
            
        feedback_data.update({
                "user_id":request.user.id,
                "feedback_type":feedback_type,
                "feedback_name":feedback_name,
                "academic_year":academic_year,
                "audience":audience,
                "start_date":start_date,
                "start_time":start_time,
                "end_date":end_date,
                "end_time":end_time,
                "current_datetime":now
            })
            
        feedbackhelper.save_feedback_details(**feedback_data)

        return HttpResponseRedirect("/feedback/create_feedback")

def feedbacklist(request):
    context = {}
    user_status = commonhelper.get_login_user_common_context(request.user,context)
    user_status=1
    if user_status == 1:
        
        inputdata = {}
        inputdata['search'] = ''
        inputdata['currentpage'] = 1
        inputdata['pagesize'] = 10
        inputdata['sort_col'] = 'fb.created_datetime'
        inputdata['sort_dir'] = 'DESC'
        inputdata['course'] = ''
        inputdata['batch'] = ''

        if request.method == 'POST':

            if 'search' in request.POST.dict() and request.POST.get('search', '') != '':
                inputdata['search'] = request.POST.get('search', '')
            if 'currentpage' in request.POST.dict() and request.POST.get('currentpage', '') != '':
                inputdata['currentpage'] = int(request.POST.get('currentpage', 1))
            if 'sort_col' in request.POST.dict() and request.POST.get('sort_col', '') != '':
                inputdata['sort_col'] = request.POST.get('sort_col', 'fb.created_datetime')
            if 'sort_dir' in request.POST.dict() and request.POST.get('sort_dir', '') != '':
                inputdata['sort_dir'] = request.POST.get('sort_dir', 'DESC')
            if 'course' in request.POST.dict() and request.POST.get('course', '') != '':
                inputdata['course'] = request.POST.get('course', '')
            if 'batch' in request.POST.dict() and request.POST.get('batch', '') != '':
                inputdata['batch'] = request.POST.get('batch', '')
            

            if 'prevsearch' in request.POST and request.POST['prevsearch'] != '/' and \
                    request.POST['prevsearch'] != inputdata['search']:
                inputdata['currentpage'] = 1
            if 'prev_course' in request.POST and request.POST['prevdate_course'] != '/' and \
                    request.POST['prevdate_course'] != inputdata['course']:
                inputdata['currentpage'] = 1
            if 'prev_batch' in request.POST and request.POST['prev_batch'] != '/' and \
                    request.POST['prev_batch'] != inputdata['batch']:
                inputdata['currentpage'] = 1

     
        records = feedbackhelper.getfeedbacklist(request, inputdata)
        context['data'] = records
       

        context['search'] = inputdata['search']
        # context['action_code'] = inputdata['action_code']
        context['course'] = inputdata['course']
        context['batch'] = inputdata['batch']

        context = commonhelper.get_login_user_common_context(request.user, context)
       
        response = HttpResponse(render(request, 'feedback/feedbacklist.html', context))
        return response
    else:
        messages.add_message(request, messages.WARNING,
                             'Please login and then proceed.')
        return HttpResponseRedirect("/accounts/login")

def submit_feedback(request):
    context = {}
    context = commonhelper.get_login_user_common_context(
        request.user, context)
   
    if request.method == 'GET':
        
        feedback_id=request.GET.get("feedback_id","")
        feedback_details=feedbackhelper.getfeedbackdetailsbyid(feedback_id)
        feedback_question_set_ids=feedbackhelper.getfeedbackquestionsetbyid(feedback_id)
        f_set=feedback_question_set_ids[0]['questions_set']
        f_set=json.loads(f_set)
        feedback_questions_set=feedbackhelper.get_all_questions_by_ids(feedback_id,tuple(f_set))
        context['feedback_questions_set']=feedback_questions_set
        context['f_set']=json.dumps(f_set)
        context['feedback_id']=feedback_id
        context["feedback_for"]=feedback_details[0]["feedback_for"]
       
        if feedback_details[0]["feedback_for"]=="Academic - Teacher":
             
            course_data=commonhelper.getallcourse()
            semester_data=commonhelper.getallsemester()
            ayear_data=commonhelper.getallacademicyear()
            faculty_data=commonhelper.getallfacultydetails()
            pattern_data=commonhelper.getallpatterns()
            division_data=commonhelper.getalldivision()
            context["course_details"]=course_data
            context["ayear_data"]=ayear_data
            context["semester_details"]=semester_data
            context["faculty_details"]=faculty_data
            context["pattern_details"]=pattern_data
            context["division_data"]=division_data
            return render(request,'feedback/submit_feedback_teacher.html',context)
        else:
            return render(request,'feedback/submit_feedback.html',context)
    if request.method == 'POST':
        
        feedback_id=request.POST.get("feedback_id","") 
        feedback_for=request.POST.get("feedback_for","") 
        if feedback_for !="Academic - Teacher":
            user_id=request.user.id
            final_records=[]
            f_set=request.POST.get('f_set','')
            f_set=json.loads(f_set)

            for item in f_set:
                answers={}
                answers.update({
                    "user_id":user_id,
                    "feedback_id":request.POST.get('feedback_id',''),
                    "question_id":item,
                    "answer_id":request.POST.get(item,'')
                    })
                final_records.append(answers)
        
            feedbackhelper.save_feedback_answers(final_records)
        if feedback_for == "Academic - Teacher":
            user_id=request.user.id
            final_records=[]
            f_set=request.POST.get('teacher_feedback_list','')
            f_set=json.loads(f_set)
            
            feedback_summary={}
            feedback_summary.update({
                "ay_id":f_set[0]["ay_id"],
                "course_id":f_set[0]["course_id"],
                "pattern_id":f_set[0]["pattern_id"],
                "sem_id":f_set[0]["sem_id"],
                "div_id":f_set[0]["div_id"],
                "submitted_datetime":datetime.now(),
                "submitted_by_userid":request.user.id,
            })
            
            last_inserted_summary_id=feedbackhelper.save_teacher_feedback_summary(feedback_summary)

            for item in f_set:
                
                for ans in item["answers"]:
                    answers={}
                    answers.update({
                        "user_id":user_id,
                        "feedback_id":feedback_id,
                        "question_id":ans["question_id"],
                        "answer_id":ans["answer_id"],
                        "faculty_id":item["faculty_id"],
                        "subject_id":item["subject_id"],
                        "teacher_feedback_summary_id":last_inserted_summary_id
                        })
                    final_records.append(answers)
           

            print(final_records)
            
            status=feedbackhelper.save_teacher_feedback_answers(final_records)
            if status:
                pass
        return HttpResponseRedirect('/student/studentdashboard')

def add_questions_to_feedback(request):
    context = {}
    context = commonhelper.get_login_user_common_context(
        request.user, context)
   
    feedback_id=request.GET.get('feedback_id','')
    if request.method =="GET":
        

        feedback_details=feedbackhelper.getfeedbackdetailsbyid(feedback_id)
        feedback_questions=feedbackhelper.getfeedbackquestionsbyid(feedback_details[0]['feedback_type_id'],feedback_details[0]['audience_id'] )
        context['feedback_details']=feedback_details
        context['feedback_questions']=feedback_questions
        context['feedback_id']=feedback_id
       
        return render(request,'feedback/add_questions_to_feedback.html',context)
    if request.method == 'POST':
   
       feedback_id=request.POST.get('feedback_id','')
       selected_question_list=json.loads(request.POST.get('selected_questions_list',""))
       temp_dict=dict(sorted(selected_question_list.items(), key=lambda x:x[1]))
       list_to_store=json.dumps(list(key for key,value in temp_dict.items()))
       now = datetime.now()
       now.strftime('%m/%d/%Y')
             
       feedback_question_data={}
       feedback_question_data.update({
                "feedback_id":feedback_id,
                "questions_set":list_to_store,
                "current_datetime":now,
                "user_id":request.user.id,
            })
       feedbackhelper.save_feedback_question_details(**feedback_question_data)
     
       return HttpResponseRedirect("/feedback/feedbacklist")

def addscale(request):
    context = {}
    context = commonhelper.get_login_user_common_context(request.user, context)
    if request.method =="GET":
        return render(request,'feedback/add_scale.html',context)
    if request.method == 'POST':
       
        txt_scale_name=request.POST.get('txt_scale_name','')
        txt_param_1=request.POST.get('txt_param_1','')
        txt_param_2=request.POST.get('txt_param_2','')
        txt_param_3=request.POST.get('txt_param_3','')
        txt_param_4=request.POST.get('txt_param_4','')
        txt_param_5=request.POST.get('txt_param_5','')
        txt_param_6=request.POST.get('txt_param_6','')
        txt_param_7=request.POST.get('txt_param_7','')
        txt_param_8=request.POST.get('txt_param_8','')
        txt_param_9=request.POST.get('txt_param_9','')
        txt_param_10=request.POST.get('txt_param_10','')

        feedback_scale_data={}

        feedback_scale_data.update({
                "user_id":request.user.id,
                "txt_scale_name":txt_scale_name,
                "txt_param_1":txt_param_1,
                "txt_param_2":txt_param_2,
                "txt_param_3":txt_param_3,
                "txt_param_4":txt_param_4,
                "txt_param_5":txt_param_5,
                "txt_param_6":txt_param_6,
                "txt_param_7":txt_param_7,
                "txt_param_8":txt_param_8,
                "txt_param_9":txt_param_9,
                "txt_param_10":txt_param_10,
            })
            
        feedbackhelper.save_feedback_scale(**feedback_scale_data)

        return HttpResponseRedirect("/feedback/addscale")

def subject_allocation(request):
    context = {}
    context = commonhelper.get_login_user_common_context(
        request.user, context)
    if request.method == 'GET':
        course_data=commonhelper.getallcourse()
        semester_data=commonhelper.getallsemester()
        ayear_data=commonhelper.getallacademicyear()
        faculty_data=commonhelper.getallfacultydetails()
        pattern_data=commonhelper.getallpatterns()
        division_data=commonhelper.getalldivision()
        context["course_details"]=course_data
        context["ayear_data"]=ayear_data
        context["semester_details"]=semester_data
        context["faculty_details"]=faculty_data
        context["pattern_details"]=pattern_data
        context["division_data"]=division_data
        return render(request,'feedback/subject_allocation.html',context)
    if request.method == 'POST':
        current_allocation_list=request.POST.get("current_allocation_list","")
        if current_allocation_list:
            current_allocation_list=json.loads(current_allocation_list)
        print(current_allocation_list)
        feedbackhelper.save_subject_allocation(request,current_allocation_list)
        return HttpResponseRedirect("/feedback/subject_allocation")

def subject_allocation_list(request):
    context = {}
    user_status = commonhelper.get_login_user_common_context(request.user,context)
    course_data=commonhelper.getallcourse()
    pattern_data=commonhelper.getallpatterns()
    semester_data=commonhelper.getallsemester()
    context["course_data"]=course_data
    context["pattern_data"]=pattern_data
    context["semester_data"]=semester_data
    user_status=1
    if user_status == 1:
       
        inputdata = {}
        inputdata['search'] = ''
        inputdata['currentpage'] = 1
        inputdata['pagesize'] = 10

        inputdata['sort_col'] = 'sub_alloc.created_datetime'
        inputdata['sort_dir'] = 'DESC'
        inputdata['course'] = ''
        inputdata['pattern'] = ''
        inputdata['semester'] = ''
        # inputdata['subject'] = ''
       
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
            if 'pattern' in request.POST.dict() and request.POST.get('pattern', '') != '':
                inputdata['pattern'] = request.POST.get('pattern', '')
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
            if 'prev_pattern' in request.POST and request.POST['prev_pattern'] != '/' and \
                    request.POST['prev_pattern'] != inputdata['pattern']:
                inputdata['currentpage'] = 1
            if 'prev_semester' in request.POST and request.POST['prev_semester'] != '/' and \
                    request.POST['prev_semester'] != inputdata['semester']:
                inputdata['currentpage'] = 1
            # if 'prev_subject' in request.POST and request.POST['prev_subject'] != '/' and \
            #         request.POST['prev_subject'] != inputdata['subject']:
            #     inputdata['currentpage'] = 1
        
        records = feedbackhelper.getall_subject_allocation_list(request, inputdata)
        
        context["data"] = records
        context["search"] = inputdata['search']
        context["course"] = inputdata['course']
        context["pattern"] = inputdata['pattern']
        context["semester"] = inputdata['semester']
        # context["subject"] = inputdata['subject']
       
        context = commonhelper.get_login_user_common_context(request.user, context)
        response = HttpResponse(render(request, 'feedback/subject_allocation_list.html', context))
        return response
    else:
        messages.add_message(request, messages.WARNING,
                             'Please login and then proceed.')
        return HttpResponseRedirect("/accounts/login") 

def get_all_faculty_by_course_pattern_sem_div(request):
    start_time = time.time()
    res = {}
    res['success'] = False
    res['message'] = ''
    data = dict()
   
    try:
        if request.method == 'POST':
            # import pdb;pdb.set_trace()
            ay_id=request.POST.get('ay_id','')
            course_id=request.POST.get('course_id','')
            pattern_id=request.POST.get('pattern_id','')
            sem_id=request.POST.get('sem_id','')
            subject_id=request.POST.get('subject_id','')
            div_id=request.POST.get('div_id','')
            faculty_data=commonhelper.get_all_faculty_by_course_pattern_sem_div(ay_id,course_id,pattern_id,sem_id,div_id)

            if faculty_data:
                res['success']=True
                res['message'] = "faculty data exists"
            else:
                res['success']=False
                res['message'] = "faculty data does not exists"
    except Exception as ex:

        res['message'] = str(ex)
    finally:
        stop_time = time.time()
        total_time = int((stop_time - start_time) * 1000)
        data = {'success': res['success'], 'timeInMillis': total_time, 'message': res['message'],'data':faculty_data}
        return JsonResponse(data)   

def get_faculty_by_course_pattern_sem_sub_div(request):
    start_time = time.time()
    res = {}
    res['success'] = False
    res['message'] = ''
    data = dict()
   
    try:
        if request.method == 'POST':
            ay_id=request.POST.get('ay_id','')
            course_id=request.POST.get('course_id','')
            pattern_id=request.POST.get('pattern_id','')
            sem_id=request.POST.get('sem_id','')
            subject_id=request.POST.get('subject_id','')
            div_id=request.POST.get('div_id','')
            faculty_data=commonhelper.get_faculty_by_course_pattern_sem_sub_div(ay_id,course_id,pattern_id,sem_id,subject_id,div_id)
            if faculty_data:
                res['success']=True
                res['message'] = "faculty data exists"
            else:
                res['success']=False
                res['message'] = "faculty data does not exists"
    except Exception as ex:

        res['message'] = str(ex)
    finally:
        stop_time = time.time()
        total_time = int((stop_time - start_time) * 1000)
        data = {'success': res['success'], 'timeInMillis': total_time, 'message': res['message'],'data':faculty_data}
        return JsonResponse(data)   

def feedback_report(request):
    context = {}
    user_status = commonhelper.get_login_user_common_context(request.user,context)
    course_data=commonhelper.getallcourse()
    pattern_data=commonhelper.getallpatterns()
    semester_data=commonhelper.getallsemester()
    context["course_data"]=course_data
    context["pattern_data"]=pattern_data
    context["semester_data"]=semester_data
    user_status=1
    if user_status == 1:
       
        inputdata = {}
        inputdata['search'] = ''
        inputdata['currentpage'] = 1
        inputdata['pagesize'] = 10

        inputdata['sort_col'] = 'f.created_datetime'
        inputdata['sort_dir'] = 'DESC'
        inputdata['course'] = ''
        inputdata['pattern'] = ''
        inputdata['semester'] = ''
        # inputdata['subject'] = ''
       
        if request.method == 'POST':
           
            if 'search' in request.POST.dict() and request.POST.get('search', '') != '':
                inputdata['search'] = request.POST.get('search', '')
            if 'currentpage' in request.POST.dict() and request.POST.get('currentpage', '') != '':
                inputdata['currentpage'] = int(request.POST.get('currentpage', 1))
            if 'sort_col' in request.POST.dict() and request.POST.get('sort_col', '') != '':
                inputdata['sort_col'] = request.POST.get('sort_col', 'f.created_datetime')
            if 'sort_dir' in request.POST.dict() and request.POST.get('sort_dir', '') != '':
                inputdata['sort_dir'] = request.POST.get('sort_dir', 'DESC')
            # if 'course' in request.POST.dict() and request.POST.get('course', '') != '':
            #     inputdata['course'] = request.POST.get('course', '')
            # if 'pattern' in request.POST.dict() and request.POST.get('pattern', '') != '':
            #     inputdata['pattern'] = request.POST.get('pattern', '')
            # if 'semester' in request.POST.dict() and request.POST.get('semester', '') != '':
            #     inputdata['semester'] = request.POST.get('semester', '')
            # if 'subject' in request.POST.dict() and request.POST.get('subject', '') != '':
            #     inputdata['subject'] = request.POST.get('subject', '')
            
            if 'prev_search' in request.POST and request.POST['prev_search'] != '/' and \
                    request.POST['prev_search'] != inputdata['search']:
                inputdata['currentpage'] = 1
        
            # if 'prev_course' in request.POST and request.POST['prev_course'] != '/' and \
            #         request.POST['prev_course'] != inputdata['course']:
            #     inputdata['currentpage'] = 1
            # if 'prev_pattern' in request.POST and request.POST['prev_pattern'] != '/' and \
            #         request.POST['prev_pattern'] != inputdata['pattern']:
            #     inputdata['currentpage'] = 1
            # if 'prev_semester' in request.POST and request.POST['prev_semester'] != '/' and \
            #         request.POST['prev_semester'] != inputdata['semester']:
            #     inputdata['currentpage'] = 1
            # if 'prev_subject' in request.POST and request.POST['prev_subject'] != '/' and \
            #         request.POST['prev_subject'] != inputdata['subject']:
            #     inputdata['currentpage'] = 1
        
        records = feedbackhelper.get_feedback_report_data(request, inputdata)
        
        context["data"] = records
        context["search"] = inputdata['search']
        # context["course"] = inputdata['course']
        # context["pattern"] = inputdata['pattern']
        # context["semester"] = inputdata['semester']
        # context["subject"] = inputdata['subject']
       
        context = commonhelper.get_login_user_common_context(request.user, context)
        response = HttpResponse(render(request, 'feedback/feedback_report.html', context))
        return response
    else:
        messages.add_message(request, messages.WARNING,
                             'Please login and then proceed.')
        return HttpResponseRedirect("/accounts/login") 

def feedback_details(request):
    context = {}
    user_status = commonhelper.get_login_user_common_context(request.user,context)

    inputdata={}
    inputdata["feedback_id"]=""
    inputdata["academic_year"]=""
    inputdata["usertype"]=""
    inputdata["course"]=""
    inputdata["pattern"]=""
    inputdata["semester"]=""
    inputdata["division"]=""
    inputdata["audience"]=""

    if request.method=="GET":
        
        feedback_id=request.GET.get("feedback_id","")
        inputdata["feedback_id"]=feedback_id
        feedback_details=feedbackhelper.get_feedback_details_by_id(inputdata["feedback_id"])
        if feedback_details:
            feedback_question_set_ids=feedbackhelper.getfeedbackquestionsetbyid(inputdata["feedback_id"])
            f_set=feedback_question_set_ids[0]['questions_set']
            f_set=json.loads(f_set)
            feedback_questions_set=feedbackhelper.get_all_questions_by_ids(inputdata["feedback_id"],tuple(f_set))
            answer_count=feedbackhelper.getquestionwiseanswersummary(inputdata)
           
            total_counts={}
            question_id=''
            for item in f_set:
                question_id=item
                count=0
                for ans in answer_count:
                    if str(ans["question_id"])==item:
                        count+=ans["answer_count"]
                total_counts.update({question_id:count})
            
            
           
            data={}
            final_dict={}
            
            
            for qu in feedback_questions_set:
                chartdata=[]
                labels = [] 
                chartLabel = qu["question"]
                
                if qu["param1"] and qu["param1"]!='' and qu["param1"] is not None:
                    labels.append(qu["param1"])
                if qu["param2"] and qu["param2"]!='' and qu["param2"] is not None:
                    labels.append(qu["param2"])
                if qu["param3"] and qu["param3"]!='' and qu["param3"] is not None:
                    labels.append(qu["param3"])
                if qu["param4"] and qu["param4"]!='' and qu["param4"] is not None:
                    labels.append(qu["param4"])
                if qu["param5"] and qu["param5"]!='' and qu["param5"] is not None:
                    labels.append(qu["param5"])
                if qu["param6"] and qu["param6"]!='' and qu["param6"] is not None:
                    labels.append(qu["param6"])
                if qu["param7"] and qu["param7"]!='' and qu["param7"] is not None:
                    labels.append(qu["param7"])
                if qu["param8"] and qu["param8"]!='' and qu["param8"] is not None:
                    labels.append(qu["param8"])
                if qu["param9"] and qu["param9"]!='' and qu["param9"] is not None:
                    labels.append(qu["param9"])
                if qu["param10"] and qu["param10"]!='' and qu["param10"] is not None:
                    labels.append(qu["param10"])

                param1=0
                param2=0
                param3=0
                param4=0
                param5=0
                param6=0
                param7=0
                param8=0
                param9=0
                param10=0
                
                for item in answer_count:
                    if item["question_id"]==qu["id"]:
                        if item["answer_id"]==1:
                            param1=item["answer_count"]
                        elif item["answer_id"]==2:
                            param2=item["answer_count"]
                        elif item["answer_id"]==3:
                            param3=item["answer_count"]
                        elif item["answer_id"]==4:
                            param4=item["answer_count"]
                        elif item["answer_id"]==5:
                            param5=item["answer_count"]
                        elif item["answer_id"]==6:
                            param6=item["answer_count"]
                        elif item["answer_id"]==7:
                            param7=item["answer_count"]
                        elif item["answer_id"]==8:
                            param8=item["answer_count"]
                        elif item["answer_id"]==9:
                            param9=item["answer_count"]
                        elif item["answer_id"]==10:
                            param10=item["answer_count"]

                
                if param1==0:
                    param1=0
                else:
                    param1=round(param1*100/total_counts[str(qu["id"])],2)
                if param2==0:
                    param2=0
                else:
                    param2=round(param2*100/total_counts[str(qu["id"])],2)
                if param3==0:
                    param3=0
                else:
                    param3=round(param3*100/total_counts[str(qu["id"])],2)
                if param4==0:
                    param4=0
                else:
                    param4=round(param4*100/total_counts[str(qu["id"])],2)
                if param5==0:
                    param5=0
                else:
                    param5=round(param5*100/total_counts[str(qu["id"])],2)
                if param6==0:
                    param6=0
                else:
                    param6=round(param6*100/total_counts[str(qu["id"])],2)
                if param7==0:
                    param7=0
                else:
                    param7=round(param7*100/total_counts[str(qu["id"])],2)
                if param8==0:
                    param8=0
                else:
                    param8=round(param8*100/total_counts[str(qu["id"])],2)
                if param9==0:
                    param9=0
                else:
                    param9=round(param9*100/total_counts[str(qu["id"])],2)
                if param10==0:
                    param10=0
                else:
                    param10=round(param10*100/total_counts[str(qu["id"])],2)
                    
                for i in range (len(labels)):
                    if i==0:
                        chartdata.append(param1)
                    elif i==1:
                        chartdata.append(param2)
                    elif i==2:
                        chartdata.append(param3)
                    elif i==3:
                        chartdata.append(param4)
                    elif i==4:
                        chartdata.append(param5)
                    elif i==5:
                        chartdata.append(param6)
                    elif i==6:
                        chartdata.append(param7)
                    elif i==7:
                        chartdata.append(param8)
                    elif i==8:
                        chartdata.append(param9)
                    elif i==9:
                        chartdata.append(param10)
                
                c_data=[list(item) for item in zip(labels,chartdata)]
                                   
                
                final_dict.update({qu["id"]:{'labels':labels,'chartLabel':chartLabel,'chartdata':chartdata,'c_data':c_data}})
            
            data.update({'student':final_dict})       
            context['data']=data
            return render(request,'feedback/feedback_details1.html',context)
    if request.method =="POST":
        pass    
    