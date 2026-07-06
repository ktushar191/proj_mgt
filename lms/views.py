from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from lms import lmshelper
from helpermodule import studenthelper,commonhelper
from feedback import feedbackhelper
from django.core.files.storage import FileSystemStorage
from datetime import datetime
from django.conf import settings

def lmsdashboard(request):
    context = {}
    user_status = commonhelper.get_login_user_common_context(request.user,context)
    if request.method == 'GET':
        return render(request,'lms/lmsdashboard1.html',context)
    if request.method == 'POST':
        pass

def notes(request):
    context = {}
    user_status = commonhelper.get_login_user_common_context(request.user,context)
    if request.method == 'GET':
        return render(request,'lms/lms_notes.html',context)
    if request.method == 'POST':
       pass

def lms_studycontent(request):

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

        inputdata['sort_col'] = 'lc.created_datetime'
        inputdata['sort_dir'] = 'DESC'
        inputdata['course'] = ''
        inputdata['pattern'] = ''
        inputdata['sem'] = ''
        inputdata['subject'] = ''

       

        if request.method == 'GET':
            pass

        if request.method == 'POST':
            
            print(request.POST.dict())
            if 'search' in request.POST.dict() and request.POST.get('search', '') != '':
                inputdata['search'] = request.POST.get('search', '')
            if 'currentpage' in request.POST.dict() and request.POST.get('currentpage', '') != '':
                inputdata['currentpage'] = int(request.POST.get('currentpage', 1))
            if 'sort_col' in request.POST.dict() and request.POST.get('sort_col', '') != '':
                inputdata['sort_col'] = request.POST.get('sort_col', 'lc.created_datetime')
            if 'sort_dir' in request.POST.dict() and request.POST.get('sort_dir', '') != '':
                inputdata['sort_dir'] = request.POST.get('sort_dir', 'DESC')
            if 'course' in request.POST.dict() and request.POST.get('course', '') != '':
                inputdata['course'] = request.POST.get('course', '')
            if 'pattern' in request.POST.dict() and request.POST.get('pattern', '') != '':
                inputdata['pattern'] = request.POST.get('pattern', '')
            if 'sem' in request.POST.dict() and request.POST.get('sem', '') != '':
                inputdata['sem'] = request.POST.get('sem', '')
            if 'subject' in request.POST.dict() and request.POST.get('subject', '') != '':
                inputdata['subject'] = request.POST.get('subject', '')
            
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
                    request.POST['prev_semester'] != inputdata['sem']:
                inputdata['currentpage'] = 1
            
            if 'prev_subject' in request.POST and request.POST['prev_subject'] != '/' and \
                    request.POST['prev_subject'] != inputdata['subject']:
                inputdata['currentpage'] = 1
           
    
        records = lmshelper.getallstudycontent(request, inputdata)
        context["data"] = records
        context["search"] = inputdata['search']
        context["course"] = inputdata['course']
        context["pattern"] = inputdata['pattern']
        context["sem"] = inputdata['sem']
        context["subject"] = inputdata['subject']

        context = commonhelper.get_login_user_common_context(request.user, context)
        response = HttpResponse(render(request, 'lms/lms_studycontent.html', context))
        return response
    else:
        messages.add_message(request, messages.WARNING,
                             'Please login and then proceed.')
        return HttpResponseRedirect("/accounts/login")
       
def PYQ(request):
    context = {}
    user_status = commonhelper.get_login_user_common_context(request.user,context)
    if request.method == 'GET':
        return render(request,'lms/lms_PYQ.html',context)
    if request.method == 'POST':
       pass

def other(request):
    context = {}
    user_status = commonhelper.get_login_user_common_context(request.user,context)
    if request.method == 'GET':
        return render(request,'lms/lms_other.html',context)
    if request.method == 'POST':
       pass
def lmscertificate(request):
    context = {}
    user_status = commonhelper.get_login_user_common_context(request.user,context)
    if request.method == 'GET':
        return render(request,'lms/lms_online_certificate.html',context)
    if request.method == 'POST':
       pass

def lmsaptitude(request):
    context = {}
    user_status = commonhelper.get_login_user_common_context(request.user,context)
    if request.method == 'GET':
        return render(request,'lms/lms_aptitude.html',context)
    if request.method == 'POST':
       pass
   

def lmssyllabus(request):
    context = {}
    user_status = commonhelper.get_login_user_common_context(request.user,context)
    if request.method == 'GET':
        return render(request,'lms/lms_syllabus.html',context)
    if request.method == 'POST':
       pass

def addcontent(request):
    context = {}
    context = commonhelper.get_login_user_common_context(request.user,context)
    if request.method == 'GET':
        course_data=commonhelper.getallcourse()
        pattern_data=commonhelper.getallpatterns()
        semester_data=commonhelper.getallsemester()
       

        context["course_data"]=course_data
        context["pattern_data"]=pattern_data
        context["semester_data"]=semester_data
        
        return render(request, 'lms/addcontent.html', context)
    if request.method == 'POST':
       
        content_link1=""
        content_link2=""
        content_title=request.POST.get("txt_title","")
        course_id = request.POST.get("course", "")
        pattern_id = request.POST.get("pattern", "")
        sem_id = request.POST.get("sem", "")
        subject_id = request.POST.get("subject", "")
        chapter = request.POST.get("chapter", "")
        content_type = request.POST.get("content_type", "")
        filestobeuploaded=request.POST.get("filetobeuploaded","")

        if content_type and content_type!='' and content_type!=None:
            if content_type == "ppt" or content_type =="txt":
                myfile = request.FILES['file_upload']
                fs = FileSystemStorage()
                filename = fs.save(myfile.name, myfile)
                content_link1 = fs.url(filename)
            elif content_type == "video":
                content_link2 = request.POST.get("txt_url", "")


        content_data = {}

        now = datetime.now()
        now.strftime('%m/%d/%Y')
        user_id=request.user.id


        content_data.update({
            "content_title": content_title,
            "course_id": course_id,
            "pattern_id": pattern_id,
            "sem_id": sem_id,
            "subject_id": subject_id,
            "chapter": chapter,
            "content_type": content_type,
            "content_link1": content_link1,
            "content_link2": content_link2,
            "created_by_userid":user_id,
            "created_datetime":now

        })
       
        lmshelper.save_content(**content_data)
        return HttpResponseRedirect("/lms/addcontent")

def addsubjects(request):
    context = {}
    context = commonhelper.get_login_user_common_context(
        request.user, context)
    if request.method =="GET":
      
        course_ids=feedbackhelper.getallcourse()
        sem_ids=feedbackhelper.getallsemester()
        context['course_ids']=course_ids
        context['sem_ids']=sem_ids
        print(context)

        return render(request,'lms/addsubjects.html',context)
    if request.method == 'POST':
    
        subject_id=request.POST.get('subject_id','')
        subject_code=request.POST.get('subject_code','')
        subject_name=request.POST.get('subject_name','')
        subject_shortname=request.POST.get('subject_shortname','')
        subject_pattern=request.POST.get('subject_pattern','')
        course_id=request.POST.get('course_id','')
        sem_id=request.POST.get('sem_id','')
        credit_points=request.POST.get('credit_points','')
        external_marks=request.POST.get('external_marks','')
        internal_marks=request.POST.get('internal_marks','')

        subject_data={}
        if subject_id=='':
            subject_id=0
            
        subject_data.update({
                #"user_id":request.user.id,
                "subject_id":subject_id,
                "subject_code":subject_code,
                "subject_name":subject_name,
                "subject_shortname":subject_shortname,
                "subject_pattern":subject_pattern,
                "course_id":course_id,
                "sem_id":sem_id,
                "credit_points":credit_points,
                "external_marks":external_marks,
                "internal_marks":internal_marks,
            })
            
        feedbackhelper.save_subjects_details(**subject_data)

        return HttpResponseRedirect("/lms/addsubjects")
    
def lmsaptitude(request):
    context = {}
    user_status = commonhelper.get_login_user_common_context(request.user,context)
    if request.method == 'GET':
        return render(request,'lms/lms_aptitude.html',context)
    if request.method == 'POST':
       pass
    
def lms_library(request):
    context = {}
    user_status = commonhelper.get_login_user_common_context(request.user,context)
    if request.method == 'GET':
        return render(request,'lms/lms_library.html',context)
    if request.method == 'POST':
       pass

def lms_project(request):
    context = {}
    user_status = commonhelper.get_login_user_common_context(request.user,context)
    if request.method == 'GET':
        return render(request,'lms/lms_project.html',context)
    if request.method == 'POST':
        pass
