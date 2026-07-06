from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import messages
from mcqexams import mcqhelper
from helpermodule import commonhelper,studenthelper
from django.http import JsonResponse
import time
from datetime import datetime
from django.http import JsonResponse
import json

def courses(request):
    context = {}
    user_status = commonhelper.get_login_user_common_context(request.user,context)
    if request.method == 'GET':
        return render(request,'mcqexams/courses.html',context)
    if request.method == 'POST':
      
       return HttpResponseRedirect("mcqexams/mca.html")
    
def subject(request):
    context = {}
    user_status = commonhelper.get_login_user_common_context(request.user,context)
    if request.method == 'GET':
        return render(request,'mcqexams/subject.html',context)
    if request.method == 'POST':
       pass

def mca(request):
    context = {}
    user_status = commonhelper.get_login_user_common_context(request.user,context)
    if request.method == 'GET':
        return render(request,'mcqexams/mca.html',context)
    if request.method == 'POST':
       pass

def mba(request):
    context = {}
    user_status = commonhelper.get_login_user_common_context(request.user,context)
    if request.method == 'GET':
        return render(request,'mcqexams/mba.html',context)
    if request.method == 'POST':
       pass

def create_test(request):
    context = {}
    user_status = commonhelper.get_login_user_common_context(request.user,context)
    if request.method == 'GET':
        return render(request,'mcqexams/create_test.html',context)
    if request.method == 'POST':
       pass

def nextpage(request):
    context = {}
    user_status = commonhelper.get_login_user_common_context(request.user,context)
    if request.method == 'GET':
        return render(request,'mcqexams/nextpage.html',context)
    if request.method == 'POST':
       pass  

def mcqdashboard(request):
    context = {}
    context = commonhelper.get_login_user_common_context(
        request.user, context)
    if request.method == 'GET':
        return render(request,'mcqexams/mcqdashboard.html',context)
    if request.method == 'POST':
       pass 

def createmcq(request):
    context = {}
    context = commonhelper.get_login_user_common_context(
        request.user, context)
    if request.method == 'GET':
        course_data=commonhelper.getallcourse()
        semester_data=commonhelper.getallsemester()
        ayear_data=commonhelper.getallacademicyear()
        context["course_details"]=course_data
        context["ayear_data"]=ayear_data
        context["semester_details"]=semester_data
        return render(request,'mcqexams/createmcq.html',context)
    if request.method == 'POST':
       
        course_id=request.POST.get("course_select","")
        pattern=request.POST.get("pattern","")
        sem_id=request.POST.get("sem","")
        subject_id=request.POST.get("subject","")
        ayear_id=request.POST.get("ayear","")
        duration=request.POST.get("duration","")

        no_of_questions=request.POST.get("no_of_questions",0)
        if not no_of_questions:
            no_of_questions=0

        marks_for_each_questions=request.POST.get("marks_for_each_questions",0)
        if not marks_for_each_questions:
            marks_for_each_questions=0
        total_marks=request.POST.get("tot_marks",0)
        if not total_marks:
            total_marks=0
        is_negative_marking=request.POST.get("is_negative_marking",False)
        negative_marks=0
        negative_marking=False
        if is_negative_marking=='true':
            negative_marking=True
        negative_marks=request.POST.get("negative_marks","")
        if not negative_marks:
            negative_marks=0


        start_date=request.POST.get('start_date','')
        start_time=request.POST.get('start_time','')
        end_date=request.POST.get('end_date','')
        end_time=request.POST.get('end_time','')
        now = datetime.now()
      
        mcqexam_data={}
        mcqexam_data.update({
                "course_id":course_id,
                "pattern":pattern,
                "sem_id":sem_id,
                "subject_id":subject_id,
                "ayear_id":ayear_id,
                "duration":duration,
                "no_of_questions":no_of_questions,
                "marks_for_each_questions":marks_for_each_questions,
                "total_marks":total_marks,
                "negative_marking":negative_marking,
                "negative_marks":negative_marks,
                
                "start_date":start_date,
                "start_time":start_time,
                "end_date":end_date,
                "end_time":end_time,
                "created_datetime":now,
                "created_by_user_id":request.user.id

            })
        
        mcqhelper.save_mcqexam_details(**mcqexam_data)
    return HttpResponseRedirect("/mcqexams/createmcq")

def get_all_subjects_by_course_and_sem(request):
    start_time = time.time()
    res = {}
    res['success'] = False
    res['message'] = ''
    data = dict()
   
    try:
        if request.method == 'POST':
            
            course_id=request.POST.get('course_id','')
            pattern=request.POST.get('pattern','')
            sem_id=request.POST.get('sem_id','')
            course_data=commonhelper.getallsubjectsbycourseandsem(course_id,sem_id,pattern)

            if course_data:
                res['success']=True
                res['message'] = "Course data exists"
            else:
                res['success']=False
                res['message'] = "Course data exists"
    except Exception as ex:

        res['message'] = str(ex)
    finally:
        stop_time = time.time()
        total_time = int((stop_time - start_time) * 1000)
        data = {'success': res['success'], 'timeInMillis': total_time, 'message': res['message'],'data':course_data}
        return JsonResponse(data)   

def mcqlist(request):
    context = {}
    user_status = commonhelper.get_login_user_common_context(request.user,context)
    user_status=1
    if user_status == 1:
        
        inputdata = {}
        inputdata['search'] = ''
        inputdata['currentpage'] = 1
        inputdata['pagesize'] = 10
        inputdata['sort_col'] = 'mc.created_datetime'
        inputdata['sort_dir'] = 'DESC'
        inputdata['course'] = ''
       

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
           
            

            if 'prevsearch' in request.POST and request.POST['prevsearch'] != '/' and \
                    request.POST['prevsearch'] != inputdata['search']:
                inputdata['currentpage'] = 1
            if 'prev_course' in request.POST and request.POST['prevdate_course'] != '/' and \
                    request.POST['prevdate_course'] != inputdata['course']:
                inputdata['currentpage'] = 1
           

     
        records = mcqhelper.getmcqlist(request, inputdata)
        context['data'] = records
       

        context['search'] = inputdata['search']
        # context['action_code'] = inputdata['action_code']
        context['course'] = inputdata['course']
        

        context = commonhelper.get_login_user_common_context(request.user, context)
        response = HttpResponse(render(request, 'mcqexams/mcqlist.html', context))
        return response
    else:
        messages.add_message(request, messages.WARNING,
                             'Please login and then proceed.')
        return HttpResponseRedirect("/accounts/login")

def addmcqquestions(request):
    context = {}
    context = commonhelper.get_login_user_common_context(
        request.user, context)
    if request.method == 'GET':
        course_data=commonhelper.getallcourse()
        semester_data=commonhelper.getallsemester()
        ayear_data=commonhelper.getallacademicyear()
        context["course_details"]=course_data
        context["ayear_data"]=ayear_data
        context["semester_details"]=semester_data
        return render(request,'mcqexams/addmcqquestions.html',context)
    if request.method == 'POST':
        
        questions_dict_to_save={}
        questions_list=[]
        subject_details={}
        action=request.POST.get("action","")
        course_id=request.POST.get("course","")
        pattern=request.POST.get("pattern","")
        sem_id=request.POST.get("sem","")
        subject_id=request.POST.get("subject","")
        chapter_id=request.POST.get("chapter","")
      
        now = datetime.now()
        now.strftime('%m/%d/%Y')
        user_id=request.user.id

        subject_details.update({
            "action":action,
            "course_id":course_id,
            "pattern":pattern,
            "sem_id":sem_id,
            "subject_id":subject_id,
            "chapter_id":chapter_id,})
        question_dict={}
        if action == 'add':
            question=request.POST.get("question","")
            option1=request.POST.get("option1","")
            option2=request.POST.get("option2","")
            option3=request.POST.get("option3","")
            option4=request.POST.get("option4","")
            answer=request.POST.get("answer","")
            question_dict.update(
                {
                    "question":question,
                    "option1":option1,
                    "option2":option2,
                    "option3":option3,
                    "option4":option4,
                    "answer":answer,})
            questions_list.append(question_dict)
            
        if action == 'upload':
         
           my_uploaded_file = request.FILES['file_input'].read() 
           import pandas as pd
           df=pd.read_excel(my_uploaded_file)
           questions_list = df.to_dict(orient='records')
           
        questions_dict_to_save.update({
            "subject_details":subject_details, 
            "question_details":questions_list,
            "current_datetime":now,
            "user_id":user_id
        })

        mcqhelper.savemcqquestion(**questions_dict_to_save)

    return HttpResponseRedirect("/mcqexams/addmcqquestions")

def mcqresult(request):
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

        inputdata['sort_col'] = 'ms.created_datetime'
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
            
            if 'prevsearch' in request.POST and request.POST['prevsearch'] != '/' and \
                    request.POST['prevsearch'] != inputdata['search']:
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

        records = mcqhelper.getall_mcqexams_results_by_student_id(request, inputdata)
        
        context["data"] = records
        context["search"] = inputdata['search']
        context["course"] = inputdata['course']
        context["pattern"] = inputdata['pattern']
        context["semester"] = inputdata['semester']
        # context["subject"] = inputdata['subject']
       
        context = commonhelper.get_login_user_common_context(request.user, context)
        response = HttpResponse(render(request, 'mcqexams/mcqresult.html', context))
        return response
    else:
        messages.add_message(request, messages.WARNING,
                             'Please login and then proceed.')
        return HttpResponseRedirect("/accounts/login") 

def add_questions_to_mcq(request):
    context = {}
    context = commonhelper.get_login_user_common_context(
        request.user, context)
   
    mcq_id=request.GET.get('mcq_id','')
    if request.method =="GET":
        
        mcq_details=mcqhelper.getmcqdetailsbyid(mcq_id)
      
        mcq_questions=mcqhelper.getmcqquestions(mcq_details[0]['course_id'],mcq_details[0]['pattern'],mcq_details[0]['sem_id'],mcq_details[0]['subject_id'])
        context['mcq_details']=mcq_details
        context['mcq_questions']=mcq_questions
        context['mcq_id']=mcq_id
       
        return render(request,'mcqexams/add_questions_to_mcq.html',context)
    if request.method == 'POST':
       
       mcq_id=request.POST.get('mcq_id','')
       selected_question_list=json.loads(request.POST.get('selected_questions_list',""))
       temp_dict=dict(sorted(selected_question_list.items(), key=lambda x:x[1]))
       list_to_store=json.dumps(list(key for key,value in temp_dict.items()))
       now = datetime.now()
       now.strftime('%m/%d/%Y')
             
       mcq_question_data={}
       mcq_question_data.update({
                "mcq_id":mcq_id,
                "mcq_questions_set":list_to_store,
                "current_datetime":now,
                "user_id":request.user.id,
            })
       mcqhelper.save_mcq_question_details(**mcq_question_data)
     
       return HttpResponseRedirect("/mcqexams/mcqlist")

def get_all_subjects_by_course_sem_pattern(request):
    start_time = time.time()
    res = {}
    res['success'] = False
    res['message'] = ''
    data = dict()
   
    try:
        if request.method == 'POST':
           
            course_id=request.POST.get('course_id','')
            pattern_id=request.POST.get('pattern','')
            sem_id=request.POST.get('sem_id','')
           
            
            course_data=commonhelper.get_all_subjects_by_course_sem_pattern(course_id,sem_id,pattern_id)

            if course_data:
                res['success']=True
                res['message'] = "Course data exists"
            else:
                res['success']=False
                res['message'] = "Course data exists"
    except Exception as ex:

        res['message'] = str(ex)
    finally:
        stop_time = time.time()
        total_time = int((stop_time - start_time) * 1000)
        data = {'success': res['success'], 'timeInMillis': total_time, 'message': res['message'],'data':course_data}
        return JsonResponse(data)   


def mcqexam(request):
    context = {}
    context = commonhelper.get_login_user_common_context(
        request.user, context)
   
    if request.method == 'GET':
        
        mcq_id = request.GET.get('mcq_id','')
        # mcq_id=1
        
        mcq_details=mcqhelper.get_mcq_details_by_id(mcq_id)
        mcq_question_set_ids=mcqhelper.getmcqquestionsetbyid(mcq_id)
        f_set=mcq_question_set_ids[0]['mcq_question_set']
        f_set=json.loads(f_set)
        mcq_questions_set=mcqhelper.get_all_questions_by_ids(tuple(f_set))
        context['mcq_details']=mcq_details
        context['mcq_questions_set']=mcq_questions_set
        context["total_questions"]=len(mcq_questions_set)
        context['f_set']=json.dumps(f_set)
        context['mcq_id']=mcq_id
       
        return render(request,'mcqexams/mcqexam.html',context)
    if request.method == 'POST':
        
        
        user_id=request.user.id
        mcq_id=request.POST.get('mcq_id',"")
        mcq_transaction_list=request.POST.get('mcq_transaction_list','')
        final_transaction_list=json.loads(mcq_transaction_list)
        mcq_details=mcqhelper.get_mcq_details_by_id(mcq_id)

        final_summary_record={
            "mcq_id":mcq_id,
            "user_id":user_id,
            "sceduled_no_of_questions":0,
            "given_questions":0,
            "scheduled_total_marks":0,
            "given_total_marks":0,
            "marks_for_each_question":0,
            "negative_marks_for_each_question":0,
            "not_attempted_questions":0,
            "marked_as_review_questions":0,
            "attempted_questions":0,
            "no_of_correct_answers":0,
            "no_of_incorrect_answers":0,
            "total_marks_for_correct_answer":0,
            "total_negative_marks":0,
            "final_scored_marks":0,
            "created_datetime":0,
            "created_by_userid":0,
        }
        
        not_attempted_questions=0
        marked_as_review_questions=0
        attempted_questions=0
        no_of_correct_answers=0
        no_of_incorrect_answers=0
        sceduled_no_of_questions=mcq_details[0]["no_of_questions"]
        given_questions=len(final_transaction_list)
        scheduled_total_marks=mcq_details[0]["total_marks"]
        marks_for_each_question=mcq_details[0]["marks_for_each_question"]
        given_total_marks=given_questions*marks_for_each_question
        negative_marks_for_each_question=mcq_details[0]["negative_marks"]
        
        for item in final_transaction_list:
            if item["status"]==0:
                not_attempted_questions+=1
            elif item["status"]==1:
                marked_as_review_questions+=1
                if item["answer_status"]==1:
                    no_of_correct_answers+=1
                else:
                    no_of_incorrect_answers+=1
            elif item["status"]==2:
                attempted_questions+=1
                if item["answer_status"]==1:
                    no_of_correct_answers+=1
                else:
                    no_of_incorrect_answers+=1

        total_marks_for_correct_answer=no_of_correct_answers*marks_for_each_question
        total_negative_marks=no_of_incorrect_answers*negative_marks_for_each_question
        final_scored_marks=total_marks_for_correct_answer-total_negative_marks
        now = datetime.now()

        final_summary_record.update({
            "mcq_id":mcq_id,
            "user_id":user_id,
            "sceduled_no_of_questions":sceduled_no_of_questions,
            "given_questions":given_questions,
            "scheduled_total_marks":scheduled_total_marks,
            "given_total_marks":given_total_marks,
            "marks_for_each_question":marks_for_each_question,
            "negative_marks_for_each_question":negative_marks_for_each_question,
            "not_attempted_questions":not_attempted_questions,
            "marked_as_review_questions":marked_as_review_questions,
            "attempted_questions":attempted_questions,
            "no_of_correct_answers":no_of_correct_answers,
            "no_of_incorrect_answers":no_of_incorrect_answers,
            "total_marks_for_correct_answer":total_marks_for_correct_answer,
            "total_negative_marks":total_negative_marks,
            "final_scored_marks":final_scored_marks,
            "created_datetime":now,
            "created_by_userid":user_id,
        })

        last_inserted_summary_id=mcqhelper.save_mcqexam_transaction_summary(**final_summary_record)

        
        final_transaction_records=[]
        
        for item in final_transaction_list:
            answers={}
            answers.update({
                "mcq_summary_id":last_inserted_summary_id,
                "question_id":item["id"],
                "status":item["status"],
                "correct_answer":item["correct_answer"],
                "selected_answer":item["selected_answer"],
                "answer_status":item["answer_status"],
                })
            final_transaction_records.append(answers)
       
        if last_inserted_summary_id:
            mcqhelper.save_mcqexam_answers(final_transaction_records)
        print(final_transaction_list)
        return HttpResponseRedirect('/mcqexams/mcqallresult')


def mcqexamlist(request):
    
  
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

        inputdata['sort_col'] = 'mc.created_datetime'
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
            
            if 'prevsearch' in request.POST and request.POST['prevsearch'] != '/' and \
                    request.POST['prevsearch'] != inputdata['search']:
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

    
        records = mcqhelper.getallmcqexamslist(request, inputdata)
        context["data"] = records
        context["search"] = inputdata['search']
        context["course"] = inputdata['course']
        context["pattern"] = inputdata['pattern']
        context["semester"] = inputdata['semester']
        # context["subject"] = inputdata['subject']
       
        context = commonhelper.get_login_user_common_context(request.user, context)
        response = HttpResponse(render(request, 'mcqexams/mcqexamlist.html', context))
        return response
    else:
        messages.add_message(request, messages.WARNING,
                             'Please login and then proceed.')
        return HttpResponseRedirect("/accounts/login")

def mcqallresult(request):
    # import pdb;pdb.set_trace()
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

        inputdata['sort_col'] = 'ms.created_datetime'
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

        records = mcqhelper.getall_mcqexams_results(request, inputdata)
        
        context["data"] = records
        context["search"] = inputdata['search']
        context["course"] = inputdata['course']
        context["pattern"] = inputdata['pattern']
        context["semester"] = inputdata['semester']
        # context["subject"] = inputdata['subject']
       
        context = commonhelper.get_login_user_common_context(request.user, context)
        response = HttpResponse(render(request, 'mcqexams/mcqallresult.html', context))
        return response
    else:
        messages.add_message(request, messages.WARNING,
                             'Please login and then proceed.')
        return HttpResponseRedirect("/accounts/login") 