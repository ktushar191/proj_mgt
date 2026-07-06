from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import messages
import mysql.connector
from django.conf import settings


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

def generateStandardResponse(response_code, message, data={}, success=True):
    if not success:
        response_success = Constant.failed
    else:
        response_success = Constant.success
    response = {
        UiString.response_code: response_code,
        UiString.response_message: message,
        UiString.response_success: response_success,
        UiString.response_data: data
    }
    return response

def save_mcqexam_details(**kwargs):
    try:
        
        mcqexam_data=kwargs
        conn = mysql.connector.connect(**db_config)
        cur = conn.cursor()
        query = '''insert into iims_tbl_mcqexam_createmcq(course_id,pattern,sem_id,subject_id,start_date,start_time,end_date,end_time,created_datetime,created_by_user_id,ayear_id,duration_in_min,no_of_questions,marks_for_each_question,total_marks,negative_marking,negative_marks)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
        cur.execute(query,(mcqexam_data["course_id"],mcqexam_data["pattern"],mcqexam_data["sem_id"],mcqexam_data["subject_id"],mcqexam_data["start_date"],
                    mcqexam_data["start_time"],mcqexam_data["end_date"],mcqexam_data["end_time"],mcqexam_data['created_datetime'],mcqexam_data["created_by_user_id"],mcqexam_data["ayear_id"],mcqexam_data["duration"],
                    mcqexam_data["no_of_questions"],mcqexam_data["marks_for_each_questions"],mcqexam_data["total_marks"],mcqexam_data["negative_marking"],mcqexam_data["negative_marks"]))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(str(e))
        return False 
    return True

def getmcqlist(request,inputdata):
    
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

        sort_col = 'mc.created_datetime'
        sort_dir = 'DESC'
        limit_query = " LIMIT " + str(pagesize) + " OFFSET " + str(startlimit)

       
        course_query=""
        # if 'course' in inputdata and inputdata['course'] and inputdata['course'] != '':
        #     course_query = "AND t1.course = '" + str(inputdata['course']) + "' "

   
        conn = mysql.connector.connect(**db_config)
        cur = conn.cursor()
        query = '''SELECT mc.id,mc.course_id,c.course_name,mc.pattern,mc.sem_id,s.semester_name,mc.subject_id,sub.subject_name,
                    mc.start_date,mc.start_time,mc.end_date,mc.end_time,mc.created_datetime,mc.created_by_user_id,
                    mc.ayear_id,ayear,mc.duration_in_min,up.first_name,up.last_name
                    FROM iims_tbl_mcqexam_createmcq mc 
                    left join iims_tbl_course c on mc.course_id=c.id
                    left join iims_tbl_semester s on mc.sem_id=s.id
                    left join iims_tbl_subjects sub on mc.subject_id=sub.id
                    left join iims_Tbl_academic_year ay on mc.ayear_id=ay.id
                    left join user_profiles up on mc.created_by_user_id=up.user_id''' \
                    + course_query + search + ''' ORDER BY ''' \
                   + str(sort_col) + ''' ''' + str(sort_dir) + limit_query
        cur.execute(query, )
        records = dict_build(cur)
        cur.close()
        conn.close()

        conn = mysql.connector.connect(**db_config)
        cur = conn.cursor()
        query1 = ''' SELECT count(mc.id)
                        FROM iims_tbl_mcqexam_createmcq mc 
                        left join iims_tbl_course c on mc.course_id=c.id
                        left join iims_tbl_semester s on mc.sem_id=s.id
                        left join iims_tbl_subjects sub on mc.subject_id=sub.id
                        left join iims_Tbl_academic_year ay on mc.ayear_id=ay.id
                        left join user_profiles up on mc.created_by_user_id=up.user_id''' \
                    + course_query + search
        
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

def savemcqquestion(**kwargs):
    try:
        
        question_data=kwargs
        print(question_data)

        subject_details=question_data['subject_details']
        question_details=question_data['question_details']
       
        query='''insert into iims_tbl_mcq_questions(course_id,pattern,sem_id,subject_id,chapter_id,question,op1,op2,op3,op4,answer,created_datetime,created_by_user_id)values'''
        values_query=""
        for item in question_details:
            values_query='''('''
            values_query+= str(subject_details['course_id'])+",'"+str(subject_details["pattern"])+"',"+str(subject_details["sem_id"])+","+str(subject_details["subject_id"])+","+str(subject_details["chapter_id"])+",'"+str(item["question"])+"','"+str(item["option1"])+"','"+str(item["option2"])+"','"+str(item["option3"])+"','"+str(item["option4"])+"','"+str(item["answer"])+"','"+str(question_data['current_datetime'])+"',"+str(question_data['user_id']
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

def getmcqdetailsbyid(mcq_id):
    try:

        conn = mysql.connector.connect(**db_config)                
        cur = conn.cursor()
        query = '''SELECT * FROM iims_db.iims_tbl_mcqexam_createmcq mc
                    where mc.id=%s'''
        cur.execute(query,(mcq_id,))
        mcq_dict = dict_build(cur)
        cur.close()
        conn.close()
        return mcq_dict
    except Exception as e:
        return None

def getmcqquestions(course_id,pattern,sem_id,subject_id):
    try:
 
        conn = mysql.connector.connect(**db_config)                
        cur = conn.cursor()
        query = '''select * from iims_tbl_mcq_questions where course_id=%s and pattern=%s and sem_id=%s and subject_id=%s '''
        cur.execute(query,(course_id,pattern,sem_id,subject_id,))
        mcq_questions_dict = dict_build(cur)
        cur.close()
        conn.close()
        return mcq_questions_dict
    except Exception as e:
        return None

def save_mcq_question_details(**kwargs):
    try:
       
        mcq_data=kwargs
        conn = mysql.connector.connect(**db_config)
        cur = conn.cursor()
        query = '''insert into iims_tbl_mcq_question_mapping(mcq_id,mcq_question_set,created_datetime,created_by_userid)values(%s,%s,%s,%s)'''
        cur.execute(query,(mcq_data["mcq_id"],mcq_data["mcq_questions_set"],mcq_data['current_datetime'],mcq_data["user_id"]))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(str(e))
        return False 
    return True

def getmcqquestionsetbyid(mcq_id):
    try:
        
        conn = mysql.connector.connect(**db_config)                
        cur = conn.cursor()
        query = '''select mcq_question_set from iims_tbl_mcq_question_mapping where mcq_id=%s'''
        cur.execute(query,(mcq_id,))
        mcq_question_dict = dict_build(cur)
        cur.close()
        conn.close()
        return mcq_question_dict
    except Exception as e:
        return None

def get_all_questions_by_ids(mcq_ids):
    try:
        conn = mysql.connector.connect(**db_config)                
        cur = conn.cursor()
        query = '''select mcq.id,mcq.course_id,c.course_name,mcq.pattern,p.id as pattern_id,mcq.subject_id,s.subject_name,
                    mcq.chapter_id,
                    mcq.question,mcq.op1,mcq.op2,mcq.op3,mcq.op4,mcq.answer,mcq.created_by_user_id,
                    mcq.sem_id,sem.semester_name
                    from iims_tbl_mcq_questions mcq
                    left join iims_tbl_course c on mcq.course_id=c.id
                    left join iims_tbl_pattern p on mcq.pattern=p.pattern
                    left join iims_tbl_subjects s on mcq.subject_id=s.id
                    left join iims_tbl_semester sem on mcq.sem_id=sem.id
                    where mcq.id in '''+str(mcq_ids)
        cur.execute(query,)
        mcq_question_dict = dict_build(cur)
        cur.close()
        conn.close()
        return mcq_question_dict
    except Exception as e:
        return None 

def get_mcq_details_by_id(mcq_id):
    try:
        conn = mysql.connector.connect(**db_config)                
        cur = conn.cursor()
        query = '''SELECT mcq.id,mcq.course_id,c.course_name,p.id as pattern_id,mcq.pattern,mcq.sem_id,
                    s.semester_name,mcq.subject_id,sub.subject_name,
                    mcq.start_date,mcq.start_time,mcq.end_date,mcq.end_time,
                    mcq.created_datetime,mcq.created_by_user_id,mcq.ayear_id,ay.ayear,mcq.duration_in_min,
                    mcq.no_of_questions,mcq.marks_for_each_question,mcq.total_marks,mcq.negative_marking,
                    mcq.negative_marks
                    FROM iims_db.iims_tbl_mcqexam_createmcq mcq
                    left join iims_tbl_course c on mcq.course_id=c.id
                    left join iims_tbl_pattern p on mcq.pattern=p.pattern
                    left join iims_tbl_semester s on mcq.sem_id=s.id
                    left join iims_tbl_subjects sub on mcq.subject_id=sub.id
                    left join iims_tbl_academic_year ay on mcq.ayear_id=ay.id
                    where mcq.id=%s'''
        cur.execute(query,(mcq_id,))
        mcq_details_dict = dict_build(cur)
        cur.close()
        conn.close()
        return mcq_details_dict
    except Exception as e:
        return None 


def save_mcqexam_transaction_summary(**kwargs):
    try:
        
        mcqexam_data=kwargs
        conn = mysql.connector.connect(**db_config)
        cur = conn.cursor()
        query = '''insert into iims_tbl_mcq_transaction_summary(mcq_id,user_id,sceduled_no_of_questions,given_questions,scheduled_total_marks,given_total_marks,marks_for_each_question,negative_marks_for_each_question,not_attempted_questions,marked_as_review_questions,attempted_questions,no_of_correct_answers,no_of_incorrect_answers,total_marks_for_correct_answer,total_negative_marks,created_datetime,created_by_userid,final_scored_marks)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
        cur.execute(query,(mcqexam_data["mcq_id"],mcqexam_data["user_id"],mcqexam_data["sceduled_no_of_questions"],mcqexam_data["given_questions"],mcqexam_data["scheduled_total_marks"],
                    mcqexam_data["given_total_marks"],mcqexam_data["marks_for_each_question"],mcqexam_data["negative_marks_for_each_question"],mcqexam_data['not_attempted_questions'],mcqexam_data["marked_as_review_questions"],mcqexam_data["attempted_questions"],mcqexam_data["no_of_correct_answers"],
                    mcqexam_data["no_of_incorrect_answers"],mcqexam_data["total_marks_for_correct_answer"],mcqexam_data["total_negative_marks"],mcqexam_data["created_datetime"],mcqexam_data["created_by_userid"],mcqexam_data["final_scored_marks"]))
       
        last_inserted_summary_id = cur.lastrowid
        conn.commit()
        cur.close()
        conn.close()
        return last_inserted_summary_id
    except Exception as e:
        print(str(e))
        return False 
    
def save_mcqexam_answers(kwargs):
    try:
        
        answer_data=kwargs

        query=''
        query+='insert into iims_tbl_mcq_transactions(mcq_summary_id,question_id,status,correct_answer,selected_answer,answer_status)values'

        values_query=''
        for item in answer_data:
            a_list=[]
            a_list.append(item['mcq_summary_id'])
            a_list.append(int(item['question_id']))
            a_list.append(int(item['status']))
            a_list.append(int(item['correct_answer']))
            a_list.append(int(item['selected_answer']))
            a_list.append(int(item['answer_status']))

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
    
def getallmcqexamslist(request,inputdata):
    
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
            search += "lower(sub.subject_name) LIKE '%" + search_txt.lower() + "%' OR lower(sub.subject_name) LIKE '%" + \
                        search_txt.lower() + "%')"
        # print(search)
        sort_col = 'mc.created_datetime'
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
            course_query = " AND mc.course_id = '" + str(inputdata['course']) + "' "

        pattern_query = ''
        if 'pattern' in inputdata and inputdata['pattern'] and inputdata['pattern'] != '':
            pattern_query = " AND p.id= '"+ str(inputdata['pattern']) + "' "
        
        semester_query=""
        if 'semester' in inputdata and inputdata['semester'] and inputdata['semester'] != '':
            semester_query = " AND mc.sem_id = '" + str(inputdata['semester']) + "' "
        
        # subject_query=""
        # if 'subject' in inputdata and inputdata['subject'] and inputdata['subject'] != '':
        #     subject_query = " AND mc.subject_id = '" + str(inputdata['subject']) + "' "
            
   
        conn = mysql.connector.connect(**db_config)
        cur = conn.cursor()
        query = '''select mc.id,mc.course_id,c.course_name,p.id as pattern_id,mc.pattern,mc.sem_id,s.semester_name,mc.subject_id,sub.subject_code,sub.subject_name,sub.subject_short_name,
                    mc.start_date,mc.start_time,mc.end_date,mc.end_time,mc.created_datetime,mc.created_by_user_id,mc.ayear_id,ay.ayear,mc.duration_in_min,mc.no_of_questions,
                    mc.marks_for_each_question,mc.total_marks,mc.negative_marking,mc.negative_marks,au.first_name,au.last_name
                    from iims_tbl_mcqexam_createmcq mc
                    left join iims_tbl_course c on mc.course_id=c.id
                    left join iims_tbl_pattern p on mc.pattern=p.pattern
                    left join iims_tbl_semester s on mc.sem_id=s.id
                    left join iims_tbl_subjects sub on mc.subject_id=sub.id
                    left join iims_tbl_academic_year ay on mc.ayear_id=ay.id
                    left join auth_user au on mc.created_by_user_id=au.id where true''' \
                 + search + course_query + pattern_query + semester_query  + ''' ORDER BY ''' \
                + str(sort_col) + ''' ''' + str(sort_dir) + limit_query
       
        cur.execute(query, )
        records = dict_build(cur)
        cur.close()
        conn.close()
        # print(records)


        conn = mysql.connector.connect(**db_config)
        cur = conn.cursor()
        query1 = ''' select count(mc.id)
                    from iims_tbl_mcqexam_createmcq mc
                    left join iims_tbl_course c on mc.course_id=c.id
                    left join iims_tbl_pattern p on mc.pattern=p.pattern
                    left join iims_tbl_semester s on mc.sem_id=s.id
                    left join iims_tbl_subjects sub on mc.subject_id=sub.id
                    left join iims_tbl_academic_year ay on mc.ayear_id=ay.id
                    left join auth_user au on mc.created_by_user_id=au.id where true''' \
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

def getall_mcqexams_results_by_student_id(request,inputdata):
    
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
            search += "lower(sub.subject_name) LIKE '%" + search_txt.lower() + "%' OR lower(sub.subject_name) LIKE '%" + \
                        search_txt.lower() + "%')"
        # print(search)
        sort_col = 'ms.created_datetime'
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
            course_query = " AND mcq.course_id = '" + str(inputdata['course']) + "' "

        pattern_query = ''
        if 'pattern' in inputdata and inputdata['pattern'] and inputdata['pattern'] != '':
            pattern_query = " AND p.id= '"+ str(inputdata['pattern']) + "' "
        
        semester_query=""
        if 'semester' in inputdata and inputdata['semester'] and inputdata['semester'] != '':
            semester_query = " AND mcq.sem_id = '" + str(inputdata['semester']) + "' "
        
        # subject_query=""
        # if 'subject' in inputdata and inputdata['subject'] and inputdata['subject'] != '':
        #     subject_query = " AND mc.subject_id = '" + str(inputdata['subject']) + "' "
            
   
        conn = mysql.connector.connect(**db_config)
        cur = conn.cursor()
        query = '''select ms.id,ms.mcq_id,ms.user_id,ms.sceduled_no_of_questions,ms.given_questions,ms.scheduled_total_marks,ms.given_total_marks,
                    ms.marks_for_each_question,ms.negative_marks_for_each_question,ms.not_attempted_questions,ms.marked_as_review_questions,
                    ms.attempted_questions,ms.no_of_correct_answers,ms.no_of_incorrect_answers,ms.total_marks_for_correct_answer,
                    ms.total_negative_marks,ms.created_datetime,ms.created_by_userid,ms.final_scored_marks,
                    mcq.course_id,c.course_name,p.id as pattern_id,mcq.pattern,mcq.sem_id,
                    s.semester_name,mcq.subject_id,sub.subject_name,
                    mcq.start_date,mcq.start_time,mcq.end_date,mcq.end_time,
                    mcq.created_by_user_id,mcq.ayear_id,ay.ayear,mcq.duration_in_min,
                    mcq.no_of_questions,mcq.marks_for_each_question,mcq.total_marks,mcq.negative_marking,
                    mcq.negative_marks
                    from iims_tbl_mcq_transaction_summary ms
                    left join iims_tbl_mcqexam_createmcq mcq on ms.mcq_id=mcq.id
                    left join iims_tbl_course c on mcq.course_id=c.id
                    left join iims_tbl_pattern p on mcq.pattern=p.pattern
                    left join iims_tbl_semester s on mcq.sem_id=s.id
                    left join iims_tbl_subjects sub on mcq.subject_id=sub.id
                    left join iims_tbl_academic_year ay on mcq.ayear_id=ay.id
                    where ms.user_id=%s ''' \
                 + search + course_query + pattern_query + semester_query  + ''' ORDER BY ''' \
                + str(sort_col) + ''' ''' + str(sort_dir) + limit_query
       
        cur.execute(query,(request.user.id,) )
        records = dict_build(cur)
        cur.close()
        conn.close()
        # print(records)


        conn = mysql.connector.connect(**db_config)
        cur = conn.cursor()
        query1 = ''' select count(ms.id)
                    from iims_tbl_mcq_transaction_summary ms
                    left join iims_tbl_mcqexam_createmcq mcq on ms.mcq_id=mcq.id
                    left join iims_tbl_course c on mcq.course_id=c.id
                    left join iims_tbl_pattern p on mcq.pattern=p.pattern
                    left join iims_tbl_semester s on mcq.sem_id=s.id
                    left join iims_tbl_subjects sub on mcq.subject_id=sub.id
                    left join iims_tbl_academic_year ay on mcq.ayear_id=ay.id
                    where ms.user_id=%s''' \
                 + search + course_query + pattern_query + semester_query 
        
        cur.execute(query1,(request.user.id,) )
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

def getall_mcqexams_results(request,inputdata):
    
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
        sort_col = 'ms.created_datetime'
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
            course_query = " AND mcq.course_id = '" + str(inputdata['course']) + "' "

        pattern_query = ''
        if 'pattern' in inputdata and inputdata['pattern'] and inputdata['pattern'] != '':
            pattern_query = " AND p.id= '"+ str(inputdata['pattern']) + "' "
        
        semester_query=""
        if 'semester' in inputdata and inputdata['semester'] and inputdata['semester'] != '':
            semester_query = " AND mcq.sem_id = '" + str(inputdata['semester']) + "' "
        
        # subject_query=""
        # if 'subject' in inputdata and inputdata['subject'] and inputdata['subject'] != '':
        #     subject_query = " AND mc.subject_id = '" + str(inputdata['subject']) + "' "
            
   
        conn = mysql.connector.connect(**db_config)
        cur = conn.cursor()
        query = '''select ms.user_id,ms.id,ms.mcq_id,ms.sceduled_no_of_questions,ms.given_questions,ms.scheduled_total_marks,ms.given_total_marks,
                    ms.marks_for_each_question,ms.negative_marks_for_each_question,ms.not_attempted_questions,ms.marked_as_review_questions,
                    ms.attempted_questions,ms.no_of_correct_answers,ms.no_of_incorrect_answers,ms.total_marks_for_correct_answer,
                    ms.total_negative_marks,ms.created_datetime,ms.created_by_userid,ms.final_scored_marks,
                    mcq.course_id,c.course_name,p.id as pattern_id,mcq.pattern,mcq.sem_id,
                    s.semester_name,mcq.subject_id,sub.subject_name,sub.subject_short_name,
                    mcq.start_date,mcq.start_time,mcq.end_date,mcq.end_time,
                    mcq.created_by_user_id,mcq.ayear_id,ay.ayear,mcq.duration_in_min,
                    mcq.no_of_questions,mcq.marks_for_each_question,mcq.total_marks,mcq.negative_marking,
                    mcq.negative_marks,au.first_name,au.last_name
                    from iims_tbl_mcq_transaction_summary ms
                    left join iims_tbl_mcqexam_createmcq mcq on ms.mcq_id=mcq.id
                    left join iims_tbl_course c on mcq.course_id=c.id
                    left join iims_tbl_pattern p on mcq.pattern=p.pattern
                    left join iims_tbl_semester s on mcq.sem_id=s.id
                    left join iims_tbl_subjects sub on mcq.subject_id=sub.id
                    left join iims_tbl_academic_year ay on mcq.ayear_id=ay.id
                    left join auth_user au on  ms.user_id=au.id
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
        query1 = ''' select count(ms.id)
                    from iims_tbl_mcq_transaction_summary ms
                    left join iims_tbl_mcqexam_createmcq mcq on ms.mcq_id=mcq.id
                    left join iims_tbl_course c on mcq.course_id=c.id
                    left join iims_tbl_pattern p on mcq.pattern=p.pattern
                    left join iims_tbl_semester s on mcq.sem_id=s.id
                    left join iims_tbl_subjects sub on mcq.subject_id=sub.id
                    left join iims_tbl_academic_year ay on mcq.ayear_id=ay.id
                    left join auth_user au on  ms.user_id=au.id
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