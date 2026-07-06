from django.shortcuts import render
from helpermodule import commonhelper
from helpermodule import studenthelper


def employerdashboard(request):
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
        return render(request,'employer/employerdashboard.html',context)
    if request.method == 'POST':
       pass