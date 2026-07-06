from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
import mysql.connector
from django.conf import settings
import time
from datetime import datetime


db_config = {
    "host": settings.DB_CREDENTIALS['HOST'],
    "user": settings.DB_CREDENTIALS['USER'],
    "password": settings.DB_CREDENTIALS['PASSWORD'],
    "database": settings.DB_CREDENTIALS['NAME']
}
def dict_build(cursor):
    column_names = list(map(lambda x: x.lower(), [d[0] for d in cursor.description]))
    details = list(cursor.fetchall())
    result = [dict(zip(column_names, row)) for row in details]
    return result

def save_content(**kwargs):
    content_data = kwargs
    try:
        conn = mysql.connector.connect(**db_config)

        cur = conn.cursor()
        query = '''insert into lms_tbl_content(id, course_id,ay_id,sem_id,sub_id,title,topic,type_id,content,link)values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'''

        cur.execute(query, (content_data["course"], content_data["academic_year"], content_data["Semester"],
                            content_data["subject"], content_data["title"], content_data["topic"], content_data["type_id"], content_data["content"], content_data["link"]))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(str(e))
        
        return False
    return True

def getallcourse():
    conn = mysql.connector.connect(**db_config)
                           
    cur = conn.cursor()
    query = '''select * from iims_tbl_course'''
    cur.execute(query,)
    course_dict = dict_build(cur)
    cur.close()
    conn.close()
    return course_dict


def getallacademicyear():
    conn = mysql.connector.connect(**db_config)
                           
    cur = conn.cursor()
    query = '''select * from iims_tbl_academic_year'''
    cur.execute(query,)
    academic_years = dict_build(cur)
    cur.close()
    conn.close()
    return academic_years

def getallsemester():
    conn = mysql.connector.connect(**db_config)
                           
    cur = conn.cursor()
    query = '''select * from iims_tbl_semester'''
    cur.execute(query,)
    semesters = dict_build(cur)
    cur.close()
    conn.close()
    return semesters


def getallsubjects():
    conn = mysql.connector.connect(**db_config)                
    cur = conn.cursor()
    query = '''select * from iims_tbl_subjects'''
    cur.execute(query,)
    subjects = dict_build(cur)
    cur.close()
    conn.close()
    return subjects

def getallfeedbacktypes():
    try:
        conn = mysql.connector.connect(**db_config)                
        cur = conn.cursor()
        query = '''select * from iims_tbl_feedback_type'''
        cur.execute(query,)
        feedback_dict = dict_build(cur)
        cur.close()
        conn.close()
        return feedback_dict
    except Exception as e:
        return None
    
def getallaudience():
    try:
        conn = mysql.connector.connect(**db_config)                
        cur = conn.cursor()
        query = '''select * from iims_tbl_feedback_audience'''
        cur.execute(query,)
        audience_dict = dict_build(cur)
        cur.close()
        conn.close()
        return audience_dict
    except Exception as e:
        return None


def save_feedback_details(**kwargs):
    try:
     
        feedback_data=kwargs
        conn = mysql.connector.connect(**db_config)
        cur = conn.cursor()
        query = '''insert into iims_tbl_feedback(feedback_type_id,feedback_name,a_year_id,audience_id,start_date,start_time,end_date,end_time,created_datetime,created_by_userid)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
        cur.execute(query,(feedback_data["feedback_type"],feedback_data["feedback_name"],feedback_data["academic_year"],feedback_data["audience"],feedback_data["start_date"],
                    feedback_data["start_time"],feedback_data["end_date"],feedback_data["end_time"],feedback_data['current_datetime'],feedback_data["user_id"]))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(str(e))
        return False 
    return True




def getfeedbacklist(request,inputdata):
    
    try:
        totalcount = startitem = enditem = pagecount = 0
        pagesize = inputdata['pagesize']
        startlimit = (inputdata['currentpage'] - 1) * pagesize
        currentpage = inputdata['currentpage']
        search_txt = ''
        if 'search' in inputdata and inputdata['search'] and inputdata['search'] != '':
            search_txt = inputdata['search']

        search = ''
        if search_txt != '':
            search = " AND ("
            search += "lower(up.first_name) LIKE '%" + search_txt.lower() + "%' OR lower(up.last_name) LIKE '%" + \
                        search_txt.lower() + "%')"

        sort_col = 'fb.created_datetime'
        sort_dir = 'DESC'
        limit_query = " LIMIT " + str(pagesize) + " OFFSET " + str(startlimit)

        batch_query = ''
        # if 'batch' in inputdata and inputdata['batch'] and inputdata['batch'] != '':
        #     batch_query = ''' AND t1.batch= '''+ str(inputdata['batch']) + "' "
            

        course_query=""
        # if 'course' in inputdata and inputdata['course'] and inputdata['course'] != '':
        #     course_query = "AND t1.course = '" + str(inputdata['course']) + "' "

        
        conn = mysql.connector.connect(**db_config)
        cur = conn.cursor()
        query = '''select fb.* , ft.feedback_for,ft.feedback_for_shortname ,fa.audience,ay.ayear,up.first_name,up.last_name
                    from iims_tbl_feedback fb 
                    left join iims_tbl_feedback_type ft on fb.feedback_type_id=ft.id
                    left join iims_tbl_feedback_audience fa on fb.audience_id=fa.id
                    left join iims_tbl_academic_year ay on fb.a_year_id= ay.id
                    left join user_profiles up on fb.created_by_userid=up.user_id where fb.is_active=1''' \
                + batch_query + course_query + search + ''' ORDER BY ''' \
                + str(sort_col) + ''' ''' + str(sort_dir) + limit_query
        cur.execute(query, )
        records = dict_build(cur)
        cur.close()
        conn.close()

        conn = mysql.connector.connect(**db_config)
        cur = conn.cursor()
        query1 = ''' select count(fb.id)
                    from iims_tbl_feedback fb 
                    left join iims_tbl_feedback_type ft on fb.feedback_type_id=ft.id
                    left join iims_tbl_feedback_audience fa on fb.audience_id=fa.id
                    left join iims_tbl_academic_year ay on fb.a_year_id= ay.id
                    left join user_profiles up on fb.created_by_userid=up.user_id where fb.is_active=1''' \
                    + batch_query + course_query + search
        
        cur.execute(query1, )
        list = cur.fetchone()
        if list:
            totalcount = list[0]
        cur.close()
        conn.close()
        # print(totalcount)

        if totalcount > 0:
            pagecount = totalcount // pagesize
            if totalcount % pagesize > 0:
                pagecount += 1

            startitem = ((inputdata['currentpage'] - 1) * pagesize) + 1
            if ((startitem + pagesize) - 1) <= totalcount:
                enditem = (startitem + pagesize) - 1
            else:
                enditem = (startitem + (totalcount % pagesize)) - 1

        data = {}
        minrange = 1
        maxrange = pagecount + 1
        if inputdata['currentpage'] - 4 > 1:
            minrange = inputdata['currentpage'] - 4
            if inputdata['currentpage'] + 5 <= pagecount:
                maxrange = inputdata['currentpage'] + 5
        else:

            if inputdata['currentpage'] + 5 <= pagecount:
                maxrange = inputdata['currentpage'] + 5

        pagecounter = []
        # print(minrange)
        # print(maxrange)
        # print(inputdata['currentpage'])
        # print(pagecount)
        for seq in range(minrange, maxrange):
            # print(seq)
            pagecounter.append(seq)
        # print(pagecounter)

        data['totalcount'] = totalcount
        data['records'] = records
        data['pagescount'] = pagecount
        data['currentpage'] = inputdata['currentpage']
        data['startitem'] = startitem
        data['enditem'] = enditem
        data['pagerange']=pagecounter
        data['rangestart'] = minrange
        data['rangeend'] = maxrange
        data['sort_col'] = sort_col
        data['sort_dir'] = sort_dir
        # data['min_date'] = min_date
        # data['max_date'] = max_date
        # print(data)
        
        return data
    except Exception as e:
        print("Exception :" + str(e))
        return None

def getfeedbackdetailsbyid(feedback_id):
    try:
        
        conn = mysql.connector.connect(**db_config)                
        cur = conn.cursor()
        query = '''select fb.*,ft.feedback_for,ft.feedback_for_shortname,ay.ayear, 
                    fa.audience
                    from iims_tbl_feedback fb
                    left join iims_tbl_feedback_type ft on fb.feedback_type_id=ft.id
                    left join iims_tbl_academic_year ay on fb.a_year_id =ay.id
                    left join iims_tbl_feedback_audience fa on fb.audience_id=fa.id
                    where fb.id=%s'''
        cur.execute(query,(feedback_id,))
        feedback_dict = dict_build(cur)
        cur.close()
        conn.close()
        return feedback_dict
    except Exception as e:
        return None
    
def getfeedbackquestionsbyid(feedback_type_id,audience_id):
    try:
        conn = mysql.connector.connect(**db_config)                
        cur = conn.cursor()
        query = '''select q.id,q.question,q.scale_id,q.question_for,fs.scale_name,fs.param1,fs.param2,
                    fs.param3,fs.param4,fs.param5,fs.param6,fs.param7,fs.param8,fs.param9,fs.param10
                    from iims_tbl_feedback_questions q 
                    left join iims_tbl_feedback_scale fs on q.scale_id=fs.id
                    where q.question_for=%s and q.audience_id=%s'''
        cur.execute(query,(feedback_type_id,audience_id))
        feedback_question_dict = dict_build(cur)
        cur.close()
        conn.close()
        return feedback_question_dict
    except Exception as e:
        return None

def getfeedbackquestionsetbyid(feedback_id):
    try:
        
        conn = mysql.connector.connect(**db_config)                
        cur = conn.cursor()
        query = '''select questions_set from iims_tbl_feedback_question_mapping where feedback_id=%s'''
        cur.execute(query,(feedback_id,))
        feedback_question_dict = dict_build(cur)
        cur.close()
        conn.close()
        return feedback_question_dict
    except Exception as e:
        return None
    
def get_all_questions_by_ids(feedback_type_id,feedback_ids):
    try:
       
        conn = mysql.connector.connect(**db_config)                
        cur = conn.cursor()
        query = '''select q.id,q.question,q.scale_id,q.question_for,fs.scale_name,fs.param1,fs.param2,
                    fs.param3,fs.param4,fs.param5,fs.param6,fs.param7,fs.param8,fs.param9,fs.param10
                    from iims_tbl_feedback_questions q 
                    left join iims_tbl_feedback_scale fs on q.scale_id=fs.id
                    where q.id in '''+str(feedback_ids)
        cur.execute(query,)
        feedback_question_dict = dict_build(cur)
        cur.close()
        conn.close()
        return feedback_question_dict
    except Exception as e:
        return None 
    
def save_feedback_answers(kwargs):
    try:
        
        answer_data=kwargs

        query=''
        query+='insert into iims_tbl_feedback_transaction(user_id,feedback_id,question_id,answer_id)values'

        values_query=''
        for item in answer_data:
            a_list=[]
            a_list.append(item['user_id'])
            a_list.append(int(item['feedback_id']))
            a_list.append(int(item['question_id']))
            a_list.append(int(item['answer_id']))
            values_query+=str(tuple(a_list))+','
        values_query = values_query.rstrip(',')
        query+=values_query
        conn = mysql.connector.connect(**db_config)
        cur = conn.cursor()
        cur.execute(query,)
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(str(e))
        return False 
    return True

def save_feedback_question_details(**kwargs):
    try:
       
        feedback_data=kwargs
        conn = mysql.connector.connect(**db_config)
        cur = conn.cursor()
        query = '''insert into iims_tbl_feedback_question_mapping(feedback_id,questions_set,created_datetime,created_by_user_id)values(%s,%s,%s,%s)'''
        cur.execute(query,(feedback_data["feedback_id"],feedback_data["questions_set"],feedback_data['current_datetime'],feedback_data["user_id"]))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(str(e))
        return False 
    return True


def save_subjects_details(**kwargs):
    try:
 
        subject_data=kwargs
        conn = mysql.connector.connect(**db_config)
        cur = conn.cursor()
        query = '''insert into iims_tbl_subjects(subject_code,subject_name,subject_short_name,subject_pattern,course_id,sem_id,cp,external,internal)values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
        cur.execute(query,(subject_data["subject_code"],subject_data["subject_name"],subject_data["subject_shortname"],subject_data["subject_pattern"],
                    subject_data["course_id"],subject_data["sem_id"],subject_data["credit_points"],subject_data['external_marks'],subject_data["internal_marks"]))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(str(e))
        return False 
    return True

def save_feedback_scale(**kwargs):
    content_data = kwargs
   
    try:

        conn = mysql.connector.connect(**db_config)

        cur = conn.cursor()
        query = '''insert into iims_tbl_feedback_scale(scale_name,param1,param2,param3,param4,param5,param6,param7,param8,param9,param10)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''

        cur.execute(query, (content_data["txt_scale_name"], content_data["txt_param_1"], content_data["txt_param_2"], content_data["txt_param_3"],
         content_data["txt_param_4"], content_data["txt_param_5"], content_data["txt_param_6"], content_data["txt_param_7"], content_data["txt_param_8"],
         content_data["txt_param_9"],content_data["txt_param_10"]))
                    
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(str(e))
        
        return False
    return True

def get_all_scales():
    try:
        conn = mysql.connector.connect(**db_config)                
        cur = conn.cursor()
        query = '''SELECT * FROM iims_db.iims_tbl_feedback_scale'''
        cur.execute(query,)
        feedback_scale_dict = dict_build(cur)
        cur.close()
        conn.close()
        return feedback_scale_dict
    except Exception as e:
        return None 


def savefeedbackquestion(**kwargs):
    try:
       
        question_data=kwargs
        question_details=question_data['feedback_question_list']
       
        query='''insert into iims_tbl_feedback_questions(question,scale_id,question_for,is_active,audience_id,created_date,created_by_userid)values'''
        values_query=""
        for item in question_details:
            values_query='''('''
            values_query+="'"+ item['question']+"',"+str(item["scale_id"])+","+str(item["feedback_type_id"])+",True"+","+str(item["audience_id"])+",'"+str(question_data['current_datetime'])+"',"+str(question_data['user_id']
)
            values_query+='''),'''
            query+=values_query
        
        query = query.rstrip(',')      
    
        conn = mysql.connector.connect(**db_config)
        cur = conn.cursor()
        
        cur.execute(query,)
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(str(e))
        return False 
    return True

def getalldivisions():
    conn = mysql.connector.connect(**db_config)
                           
    cur = conn.cursor()
    query = '''select * from iims_tbl_division'''
    cur.execute(query,)
    divisions = dict_build(cur)
    cur.close()
    conn.close()
    return divisions

def getallbatch():
    conn = mysql.connector.connect(**db_config)
                           
    cur = conn.cursor()
    query = '''select * from iims_tbl_course_batch'''
    cur.execute(query,)
    batch_dict = dict_build(cur)
    cur.close()
    conn.close()
    return batch_dict


def save_subject_allocation(request,kwargs):
    try:
        
        allocation_data=kwargs
       
        current_datetime=datetime.now()
        query=''
        query+='insert into iims_tbl_subject_allocation(ay_id,course_id,pattern_id,sem_id,subject_id,faculty_id,created_datetime,created_by_userid,div_id)values'

        values_query=''
        for item in allocation_data:
            a_list=[]
            a_list.append(item['ay_id'])
            a_list.append(int(item['course_id']))
            a_list.append(int(item['pattern_id']))
            a_list.append(int(item['sem_id']))
            a_list.append(int(item['subject_id']))
            a_list.append(int(item['faculty_id']))
            a_list.append(str(current_datetime))
            a_list.append(request.user.id)
            a_list.append(int(item['division_id']))

            values_query+=str(tuple(a_list))+','
        values_query = values_query.rstrip(',')
        query+=values_query

       
        conn = mysql.connector.connect(**db_config)
        cur = conn.cursor()
        cur.execute(query,)
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(str(e))
        return False 
    return True

def getall_subject_allocation_list(request,inputdata):
    
    global min_date, max_date
    try:
       
        totalcount = startitem = enditem = pagecount = 0
        pagesize = inputdata['pagesize']
        startlimit = (inputdata['currentpage'] - 1) * pagesize
        currentpage = inputdata['currentpage']
        search_txt = ''
        if 'search' in inputdata and inputdata['search'] and inputdata['search'] != '':
            search_txt = inputdata['search']

        search = ''
        if search_txt != '':
            search = " AND ("
            search += "lower(sub.subject_name) LIKE '%" + search_txt.lower() + "%' OR lower(au.first_name) LIKE '%" + \
                        search_txt.lower() + "%' OR lower(au.last_name) LIKE '%" + search_txt.lower() + "%')"
        # print(search)
        sort_col = 'sub_alloc.created_datetime'
        sort_dir = 'DESC'
        limit_query = " LIMIT " + str(pagesize) + " OFFSET " + str(startlimit)
        if ('showall' in inputdata and inputdata['showall'] is not None and int(inputdata['showall']) == 1):
            limit_query = ""
        if 'sort_col' in inputdata and inputdata['sort_col'] != None:
            sort_col = inputdata['sort_col']
        if 'sort_dir' in inputdata and inputdata['sort_dir'] != None:
            sort_dir = inputdata['sort_dir']
        
        course_query=""
        if 'course' in inputdata and inputdata['course'] and inputdata['course'] != '':
            course_query = " AND sub_alloc.course_id = '" + str(inputdata['course']) + "' "

        pattern_query = ''
        if 'pattern' in inputdata and inputdata['pattern'] and inputdata['pattern'] != '':
            pattern_query = " AND sub_alloc.pattern_id= '"+ str(inputdata['pattern']) + "' "
        
        semester_query=""
        if 'semester' in inputdata and inputdata['semester'] and inputdata['semester'] != '':
            semester_query = " AND sub_alloc.sem_id = '" + str(inputdata['semester']) + "' "      
   
        conn = mysql.connector.connect(**db_config)
        cur = conn.cursor()
        query = '''select sub_alloc.id,sub_alloc.ay_id,ay.ayear,sub_alloc.course_id,c.course_name,sub_alloc.pattern_id,p.pattern,sub_alloc.sem_id,
                    s.semester_name,sub_alloc.subject_id,sub.subject_name,concat(au.first_name,' ',au.last_name)as faculty_name,
                    sub_alloc.faculty_id,sub_alloc.created_datetime,sub_alloc.created_by_userid,concat(auc.first_name,' ',auc.last_name)as created_by_username
                    from iims_tbl_subject_allocation sub_alloc
                    left join iims_tbl_academic_year ay on ay.id=sub_alloc.ay_id
                    left join iims_tbl_course c on c.id=sub_alloc.course_id
                    left join iims_tbl_pattern p on p.id=sub_alloc.pattern_id
                    left join iims_tbl_semester s on s.id=sub_alloc.sem_id
                    left join iims_tbl_subjects sub on sub.id=sub_alloc.subject_id
                    left join auth_user au on au.id=sub_alloc.faculty_id
                    left join auth_user auc on auc.id=sub_alloc.created_by_userid
                    where True  ''' \
                 + search + course_query + pattern_query + semester_query  + ''' ORDER BY ''' \
                + str(sort_col) + ''' ''' + str(sort_dir) + limit_query
       
        cur.execute(query, )
        records = dict_build(cur)
        cur.close()
        conn.close()
        # print(records)


        conn = mysql.connector.connect(**db_config)
        cur = conn.cursor()
        query1 = ''' select count(sub_alloc.id)
                    from iims_tbl_subject_allocation sub_alloc
                    left join iims_tbl_academic_year ay on ay.id=sub_alloc.ay_id
                    left join iims_tbl_course c on c.id=sub_alloc.course_id
                    left join iims_tbl_pattern p on p.id=sub_alloc.pattern_id
                    left join iims_tbl_semester s on s.id=sub_alloc.sem_id
                    left join iims_tbl_subjects sub on sub.id=sub_alloc.subject_id
                    left join auth_user au on au.id=sub_alloc.faculty_id
                    left join auth_user auc on auc.id=sub_alloc.created_by_userid
                    where True''' \
                 + search + course_query + pattern_query + semester_query 
        
        cur.execute(query1, )
        list = cur.fetchone()
        if list:
            totalcount = list[0]
        cur.close()
        conn.close()
        # print(totalcount)

        if totalcount > 0:
            pagecount = totalcount // pagesize
            if totalcount % pagesize > 0:
                pagecount += 1

            startitem = ((inputdata['currentpage'] - 1) * pagesize) + 1
            if ((startitem + pagesize) - 1) <= totalcount:
                enditem = (startitem + pagesize) - 1
            else:
                enditem = (startitem + (totalcount % pagesize)) - 1

        data = {}
        minrange = 1
        maxrange = pagecount + 1
        if inputdata['currentpage'] - 4 > 1:
            minrange = inputdata['currentpage'] - 4
            if inputdata['currentpage'] + 5 <= pagecount:
                maxrange = inputdata['currentpage'] + 5
        else:

            if inputdata['currentpage'] + 5 <= pagecount:
                maxrange = inputdata['currentpage'] + 5

        pagecounter = []
 
        for seq in range(minrange, maxrange):
            pagecounter.append(seq)
  
        data['totalcount'] = totalcount
        data['records'] = records
        data['pagescount'] = pagecount
        data['currentpage'] = inputdata['currentpage']
        data['startitem'] = startitem
        data['enditem'] = enditem
        data['pagerange']=pagecounter
        data['rangestart'] = minrange
        data['rangeend'] = maxrange
        data['sort_col'] = sort_col
        data['sort_dir'] = sort_dir
        # data['min_date'] = min_date
        # data['max_date'] = max_date
        # print(data)
        
        return data
    except Exception as e:
        print("Exception :" + str(e))
        return None

def save_teacher_feedback_answers(kwargs):
    try:
        
        answer_data=kwargs

        query=''
        query+='insert into iims_tbl_feedback_transaction(user_id,feedback_id,question_id,answer_id,faculty_id,subject_id,teacher_feedback_summary_id)values'

        values_query=''
        for item in answer_data:
            a_list=[]
            a_list.append(item['user_id'])
            a_list.append(int(item['feedback_id']))
            a_list.append(int(item['question_id']))
            a_list.append(int(item['answer_id']))
            a_list.append(int(item['faculty_id']))
            a_list.append(int(item['subject_id']))
            a_list.append(int(item['teacher_feedback_summary_id']))
            values_query+=str(tuple(a_list))+','
        values_query = values_query.rstrip(',')
        query+=values_query
        conn = mysql.connector.connect(**db_config)
        cur = conn.cursor()
        cur.execute(query,)
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(str(e))
        return False 
    return True

def save_teacher_feedback_summary(kwargs):
    try:
        
        sum_data=kwargs
        
        query=''
        query+='insert into iims_tbl_feedback_teacher_summary(ay_id,course_id,pattern_id,sem_id,div_id,submited_datetime,submitted_by_userid)values(%s,%s,%s,%s,%s,%s,%s)'
        conn = mysql.connector.connect(**db_config)
        cur = conn.cursor()
        cur.execute(query,(sum_data["ay_id"],sum_data["course_id"],sum_data["pattern_id"],sum_data["sem_id"],sum_data["div_id"],sum_data["submitted_datetime"],sum_data["submitted_by_userid"]))
        last_inserted_summary_id = cur.lastrowid
        conn.commit()
        cur.close()
        conn.close()
        return last_inserted_summary_id
    except Exception as e:
        print(str(e))
        return False 

def get_feedback_report_data(request,inputdata):
    
    global min_date, max_date
    try:
        
        totalcount = startitem = enditem = pagecount = 0
        pagesize = inputdata['pagesize']
        startlimit = (inputdata['currentpage'] - 1) * pagesize
        currentpage = inputdata['currentpage']
        search_txt = ''
        if 'search' in inputdata and inputdata['search'] and inputdata['search'] != '':
            search_txt = inputdata['search']

        search = ''
        if search_txt != '':
            search = " AND ("
            search += "lower(ft.feedback_for) LIKE '%" + search_txt.lower() + "%' OR lower(au.first_name) LIKE '%" + \
                        search_txt.lower() + "%' OR lower(au.last_name) LIKE '%" + search_txt.lower() + "%')"
        # print(search)
        sort_col = 'f.created_datetime'
        sort_dir = 'DESC'
        limit_query = " LIMIT " + str(pagesize) + " OFFSET " + str(startlimit)
        if ('showall' in inputdata and inputdata['showall'] is not None and int(inputdata['showall']) == 1):
            limit_query = ""
        if 'sort_col' in inputdata and inputdata['sort_col'] != None:
            sort_col = inputdata['sort_col']
        if 'sort_dir' in inputdata and inputdata['sort_dir'] != None:
            sort_dir = inputdata['sort_dir']
        
        # course_query=""
        # if 'course' in inputdata and inputdata['course'] and inputdata['course'] != '':
        #     course_query = " AND sub_alloc.course_id = '" + str(inputdata['course']) + "' "

        # pattern_query = ''
        # if 'pattern' in inputdata and inputdata['pattern'] and inputdata['pattern'] != '':
        #     pattern_query = " AND sub_alloc.pattern_id= '"+ str(inputdata['pattern']) + "' "
        
        # semester_query=""
        # if 'semester' in inputdata and inputdata['semester'] and inputdata['semester'] != '':
        #     semester_query = " AND sub_alloc.sem_id = '" + str(inputdata['semester']) + "' "      
   
        conn = mysql.connector.connect(**db_config)
        cur = conn.cursor()
        query = '''SELECT f.id,ft.feedback_for,f.feedback_type_id,f.a_year_id,ay.ayear,f.audience_id,fa.audience,f.start_date,f.start_time,
                    f.end_date,f.end_time,f.created_datetime,f.created_by_userid,concat(au.first_name,' ',au.last_name) created_by
                    FROM iims_db.iims_tbl_feedback f
                    left join iims_tbl_feedback_type ft on ft.id=f.feedback_type_id
                    left join iims_tbl_academic_year ay on f.a_year_id=ay.id
                    left join iims_tbl_feedback_audience fa on f.audience_id=fa.id
                    left join auth_user au on f.created_by_userid=au.id
                    where f.is_active=1  ''' \
                 + search  + ''' ORDER BY ''' \
                + str(sort_col) + ''' ''' + str(sort_dir) + limit_query
       
        cur.execute(query, )
        records = dict_build(cur)
        cur.close()
        conn.close()
        # print(records)


        conn = mysql.connector.connect(**db_config)
        cur = conn.cursor()
        query1 = ''' SELECT count(f.id)
                        FROM iims_db.iims_tbl_feedback f
                        left join iims_tbl_feedback_type ft on ft.id=f.feedback_type_id
                        left join iims_tbl_academic_year ay on f.a_year_id=ay.id
                        left join iims_tbl_feedback_audience fa on f.audience_id=fa.id
                        left join auth_user au on f.created_by_userid=au.id
                    where f.is_active=1''' \
                 + search 
        
        cur.execute(query1, )
        list = cur.fetchone()
        if list:
            totalcount = list[0]
        cur.close()
        conn.close()
        # print(totalcount)

        if totalcount > 0:
            pagecount = totalcount // pagesize
            if totalcount % pagesize > 0:
                pagecount += 1

            startitem = ((inputdata['currentpage'] - 1) * pagesize) + 1
            if ((startitem + pagesize) - 1) <= totalcount:
                enditem = (startitem + pagesize) - 1
            else:
                enditem = (startitem + (totalcount % pagesize)) - 1

        data = {}
        minrange = 1
        maxrange = pagecount + 1
        if inputdata['currentpage'] - 4 > 1:
            minrange = inputdata['currentpage'] - 4
            if inputdata['currentpage'] + 5 <= pagecount:
                maxrange = inputdata['currentpage'] + 5
        else:

            if inputdata['currentpage'] + 5 <= pagecount:
                maxrange = inputdata['currentpage'] + 5

        pagecounter = []
 
        for seq in range(minrange, maxrange):
            pagecounter.append(seq)
  
        data['totalcount'] = totalcount
        data['records'] = records
        data['pagescount'] = pagecount
        data['currentpage'] = inputdata['currentpage']
        data['startitem'] = startitem
        data['enditem'] = enditem
        data['pagerange']=pagecounter
        data['rangestart'] = minrange
        data['rangeend'] = maxrange
        data['sort_col'] = sort_col
        data['sort_dir'] = sort_dir
        # data['min_date'] = min_date
        # data['max_date'] = max_date
        # print(data)
        
        return data
    except Exception as e:
        print("Exception :" + str(e))
        return None

def get_feedback_details_by_id(feedback_id):
    try:
        
        conn = mysql.connector.connect(**db_config)                
        cur = conn.cursor()
        query = '''SELECT fb.id as feedback_id,fb.feedback_type_id,ft.feedback_for,ft.feedback_for_shortname,fb.a_year_id,ay.ayear,
                    fb.audience_id,fa.audience, fb.start_date,fb.start_time,
                    fb.end_date,fb.end_time,fb.created_datetime,fb.created_by_userid,au.first_name,au.last_name
                    FROM iims_db.iims_tbl_feedback fb
                    left join iims_tbl_feedback_type ft on fb.feedback_type_id=ft.id
                    left join iims_tbl_academic_year ay on fb.a_year_id=ay.id
                    left join iims_tbl_feedback_audience fa on fb.audience_id=fa.id
                    left join auth_user au on fb.created_by_userid=au.id where fb.id=%s'''
        cur.execute(query,(feedback_id,))
        feedback_dict = dict_build(cur)
        cur.close()
        conn.close()
        return feedback_dict
    except Exception as e:
        return None
    
def getquestionwiseanswersummary(inputdata):

    feedback_id_query=""
    if 'feedback_id' in inputdata and inputdata['feedback_id'] and inputdata['feedback_id'] != '':
            feedback_id_query = " AND ft.feedback_id = '"+ str(inputdata['feedback_id']) + "' "
    
    course_query=""
    if 'course' in inputdata and inputdata['course'] and inputdata['course'] != '':
            course_query = " AND uad.course_id = '"+ str(inputdata['course']) + "' "
    
    semester_query=""
    if 'semester' in inputdata and inputdata['semester'] and inputdata['semester'] != '':
            semester_query = " AND uad.current_semester_id = '"+ str(inputdata['semester']) + "' "
    
    divsion_query=""
    if 'division' in inputdata and inputdata['division'] and inputdata['division'] != '':
            divsion_query = " AND uad.division_id = '"+ str(inputdata['division']) + "' "

    conn = mysql.connector.connect(**db_config)                
    cur = conn.cursor()
    query = '''SELECT ft.feedback_id,
                -- ft.user_id,au.first_name,au.last_name,up.user_type,uad.course_id,
                -- uad.current_semester_id,uad.division_id,
                ft.question_id,ft.answer_id,count(answer_id)as answer_count
                FROM iims_db.iims_tbl_feedback_transaction ft
                left join auth_user au on ft.user_id=au.id
                left join user_profiles up on up.user_id=ft.user_id
                left join iims_tbl_user_academic_details uad on uad.user_id=ft.user_id
                where True'''+feedback_id_query+course_query+semester_query+divsion_query+\
                    ''' group by ft.feedback_id,ft.question_id,ft.answer_id
                order by ft.feedback_id,ft.question_id,ft.answer_id;'''
    cur.execute(query,)
    answers_count = dict_build(cur)
    cur.close()
    conn.close()
    return answers_count