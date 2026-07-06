from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import messages
import mysql.connector
from django.conf import settings
from profiles.models import SessionLog
from random import randint
from easy_thumbnails.files import get_thumbnailer
import os
import io
import PIL.Image as Image

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

def get_login_user_common_context(user, context):
    context['user_profile']=None
    if user.is_authenticated :
        username=user.username
        user_profile = getUserProfileByUser(username)
        context['user_profile'] = user_profile
    return context


def getUserProfileByUser(username):
    db_config = {
    "host": settings.DB_CREDENTIALS['HOST'],
    "user": settings.DB_CREDENTIALS['USER'],
    "password": settings.DB_CREDENTIALS['PASSWORD'],
    "database": settings.DB_CREDENTIALS['NAME']
    }
    conn = mysql.connector.connect(**db_config)            
    cur = conn.cursor()
    query = '''select au.id,au.username,au.first_name,au.last_name,au.email,au.is_superuser,au.is_staff,au.is_active,
                au.date_joined,au.last_login,up.mobile,up.user_type,up.is_mobile_verified,up.is_email_verified ,
                up.image_main_url,up.image_bigthumb_url,up.image_smallthumb_url,
                user_details.*,ufd.father_name,ufd.mother_name,ufd.no_of_siblings,ufd.fathers_occupation,
                uadd.address_line_1,uadd.address_line_2,uadd.address_line_3,uadd.country,uadd.state,uadd.district,uadd.pin
                from auth_user au left join user_profiles up on au.id=up.user_id 
                left join (select uad.user_id,uad.course_id,itc.course_name,itc.course_fees,uad.ay_year_id,ay.ayear,uad.admission_through_id, 
                adt.admission_under_name,uad.category_id,c.category,uad.previous_qualification,uad.previous_qualification_perc
                from iims_tbl_user_academic_details uad left join iims_tbl_course itc on uad.course_id=itc.id
                left join iims_tbl_academic_year ay on uad.ay_year_id=ay.id
                left join iims_tbl_admission_through adt on uad.admission_through_id=adt.id
                left join iims_tbl_category c on uad.category_id=c.id) as user_details on au.id=user_details.user_id
                left join iims_tbl_user_family_details ufd on au.id=ufd.user_id
                left join iims_tbl_user_address uadd on au.id=uadd.user_id
                where au.username=%s'''
    cur.execute(query,(username,))
    user_profile = dict_build(cur)
    cur.close()
    conn.close()
    return user_profile


def add_session_log(request, auth_type='password'):
    try:
        session_log = SessionLog.objects.create(user=request.user, client='', source='web',auth_type=auth_type)
        session_log.save()
        request.session['session_id'] = str(session_log.id)
        request.session.modified = True
    except Exception as ex:
   
        print(str(ex))
        # logger.exception(ex)
    finally:
        return None


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
    course_dict = dict_build(cur)
    cur.close()
    conn.close()
    return course_dict

def getallsemester():
    conn = mysql.connector.connect(**db_config)
                           
    cur = conn.cursor()
    query = '''select * from iims_tbl_semester'''
    cur.execute(query,)
    course_dict = dict_build(cur)
    cur.close()
    conn.close()
    return course_dict


def getallsubjects():
    conn = mysql.connector.connect(**db_config)
                           
    cur = conn.cursor()
    query = '''select * from iims_tbl_subjects'''
    cur.execute(query,)
    course_dict = dict_build(cur)
    cur.close()
    conn.close()
    return course_dict


def getadmisstionthrough(course_id):
    conn = mysql.connector.connect(**db_config)                 
    cur = conn.cursor()
    query = '''select * from iims_tbl_admission_through where for_course_id=%s'''
    cur.execute(query,(course_id,))
    admission_through_dict = dict_build(cur)
    cur.close()
    conn.close()
    return admission_through_dict

def getallcategory():
    conn = mysql.connector.connect(**db_config)
                           
    cur = conn.cursor()
    query = '''select * from iims_tbl_category'''
    cur.execute(query,)
    category_dict = dict_build(cur)
    cur.close()
    conn.close()
    return category_dict

def uploadProfileImages(posted_file, file_content,user_name):

    images = {"image_main_url": '', "image_bigthumb_url": '', "image_smallthumb_url": ''}
    try:
        content_type = posted_file.content_type
        extension = (posted_file.name.split("."))[-1]
        import time
        image_name = str(round(time.time() * 1000)) + str(random_number(4))

        # Upload main image
        images['image_main_url'] = uploadImage(posted_file,content_type, file_content, "main_"+image_name,"." + extension,user_name)

        # Upload bigthumb image
        thumbnailer_thb = get_thumbnailer(posted_file, relative_name='TempThumb_.jpeg')
        images['image_bigthumb_url'] = uploadImage(posted_file,content_type, thumbnailer_thb.generate_thumbnail(
            {'size': (150, 150), 'crop': False}, False).read(),
            "bigthumb_"+image_name, "." + extension,user_name)

        # Upload smallthumb image
        thumbnailer_ths = get_thumbnailer(
            posted_file, relative_name='TempThumb.jpeg')
        images['image_smallthumb_url'] = uploadImage(posted_file,content_type, thumbnailer_ths.generate_thumbnail(
            {'size': (40, 40), 'crop': False}, False).read(), "smallthumb_"+image_name,"." + extension,user_name)
    except Exception as ex:
        print(str(ex))
    return images

def uploadImage(posted_file,content_type, file_content, image_name,extension,user_name):
    image_url = ''
    image_url='static/images/Userprofile/' + user_name + "_" + image_name + extension
    try:
        image = Image.open(posted_file)
        image.save(image_url)
        return "/"+image_url
    except Exception as ex:
        print(str(ex))
        return ''
    
def random_number(length=3):
    return randint(10 ** (length - 1), (10 ** (length) - 1))


def getallfeedbackresults():
    conn = mysql.connector.connect(**db_config)
                           
    cur = conn.cursor()
    query = '''SELECT fr.*,fq.question,fq.scale_id,fq.audience_id,fq.is_active,fq.sequence,aa.ayear 
                FROM iims_db.iims_tbl_feedback_result fr 
                left join iims_tbl_feedback_questions fq on fr.question_id=fq.id 
                left join iims_tbl_academic_year aa on fr.a_year=aa.id
                where fq.is_active=true 
                order by sequence asc'''
    cur.execute(query,)
    feedback_dict = dict_build(cur)
    

    cur.close()
    conn.close()
    return feedback_dict

def getallfeedbackresultscount():
    conn = mysql.connector.connect(**db_config)
                 
    cur = conn.cursor()
    query = '''SELECT fr.type,count(fr.question_id) as count
                FROM iims_db.iims_tbl_feedback_result fr 
                left join iims_tbl_feedback_questions fq on fr.question_id=fq.id 
                left join iims_tbl_academic_year aa on fr.a_year=aa.id
                where fq.is_active=true 
                group by fr.type'''
    cur.execute(query,)
    feedback_result_count = dict_build(cur)
    cur.close()
    conn.close()
    return feedback_result_count



def getallsubjectsbycourseandsem(course_id,sem_id,pattern):
    conn = mysql.connector.connect(**db_config)
        
    cur = conn.cursor()
    query = '''SELECT * FROM iims_db.iims_tbl_subjects where course_id=%s and sem_id=%s and subject_pattern=%s;'''
    cur.execute(query,(course_id,sem_id,pattern))
    course_dict = dict_build(cur)
    cur.close()
    conn.close()
    return course_dict

def getallstudent_details():
    conn = mysql.connector.connect(**db_config)
                           
    cur = conn.cursor()
    query = '''select * from iims_db.user_profiles where user_type="s";'''
    cur.execute(query,)
    all_student_data_dict = dict_build(cur)
    cur.close()
    conn.close()
    return all_student_data_dict

def get_course_id_ay_id_by_userid(user_id):
    conn = mysql.connector.connect(**db_config)
                           
    cur = conn.cursor()
    query = '''SELECT user_id,course_id,ay_year_id,current_semester_id,roll_no FROM iims_db.iims_tbl_user_academic_details where user_id=%s;'''
    cur.execute(query,(user_id))
    course_dict = dict_build(cur)
    cur.close()
    conn.close()
    return course_dict

def getallroles():
    try:
        conn = mysql.connector.connect(**db_config)                
        cur = conn.cursor()
        query = '''select * from user_role'''
        cur.execute(query,)
        user_role_dict = dict_build(cur)
        cur.close()
        conn.close()
        return user_role_dict
    except Exception as e:
        return None

def getallgrade():
    try:
        conn = mysql.connector.connect(**db_config)                
        cur = conn.cursor()
        query = '''select * from iims_tbl_result_analysis_grade'''
        cur.execute(query,)
        grade_dict = dict_build(cur)
        cur.close()
        conn.close()
        return grade_dict
    except Exception as e:
        return None


def getalldivisions():
    conn = mysql.connector.connect(**db_config)
                           
    cur = conn.cursor()
    query = '''select * from iims_tbl_division'''
    cur.execute(query,)
    divisions = dict_build(cur)
    cur.close()
    conn.close()
    return divisions

def getallpatterns():
    
    conn = mysql.connector.connect(**db_config)
                           
    cur = conn.cursor()
    query = '''select * from iims_tbl_pattern'''
    cur.execute(query,)
    pattern_dict = dict_build(cur)
    cur.close()
    conn.close()
    return pattern_dict

def get_all_subjects_by_course_sem_pattern(course_id,sem_id,pattern):
    conn = mysql.connector.connect(**db_config)  
   
    cur = conn.cursor()
    query = '''SELECT sub.* FROM iims_db.iims_tbl_subjects sub
               left join iims_tbl_pattern p on sub.subject_pattern=p.pattern where sub.course_id=%s and sub.sem_id=%s and p.id=%s;'''
    cur.execute(query,(course_id,sem_id,pattern))
    course_dict = dict_build(cur)
    cur.close()
    conn.close()
    return course_dict

def getallfacultydetails():
    conn = mysql.connector.connect(**db_config)
                           
    cur = conn.cursor()
    query = '''select up.user_id,up.first_name,up.last_name,up.email,up.mobile,up.user_type
                    from user_profiles up
                    left join auth_user au on au.id=up.user_id
                    where au.is_active=true and up.user_type='f' '''
    cur.execute(query,)
    faculty_dict = dict_build(cur)
    cur.close()
    conn.close()
    return faculty_dict

def get_faculty_by_course_pattern_sem_sub_div(ay_id,course_id,pattern_id,sem_id,subject_id,div_id):
    conn = mysql.connector.connect(**db_config)  
  
    cur = conn.cursor()
    query = '''
            select sub_alloc.ay_id,sub_alloc.course_id,sub_alloc.pattern_id,sub_alloc.sem_id,
            sub_alloc.subject_id,sub_alloc.faculty_id,sub_alloc.created_datetime,sub_alloc.created_by_userid,sub_alloc.div_id,
            au.first_name,au.last_name
            from iims_tbl_subject_allocation sub_alloc
            left join auth_user au on au.id=sub_alloc.faculty_id
            where sub_alloc.ay_id=%s and sub_alloc.course_id=%s and sub_alloc.pattern_id=%s and 
            sub_alloc.sem_id=%s and sub_alloc.subject_id=%s and sub_alloc.div_id=%s '''
    cur.execute(query,(ay_id,course_id,pattern_id,sem_id,subject_id,div_id))
    faculty_dict = dict_build(cur)
    cur.close()
    conn.close()
    return faculty_dict


def get_all_faculty_by_course_pattern_sem_div(ay_id,course_id,pattern_id,sem_id,div_id):
    conn = mysql.connector.connect(**db_config)  
    
    cur = conn.cursor()
    query = '''
          select sub_alloc.id,sub_alloc.ay_id,ay.ayear,sub_alloc.course_id,c.course_name,sub_alloc.pattern_id,p.pattern,sub_alloc.sem_id,
            s.semester_name,sub_alloc.subject_id,sub.subject_name,concat(au.first_name,' ',au.last_name)as faculty_name,sub_alloc.div_id,
            sub_alloc.faculty_id,sub_alloc.created_datetime,sub_alloc.created_by_userid,concat(auc.first_name,' ',auc.last_name)as created_by_username
            from iims_tbl_subject_allocation sub_alloc
            left join iims_tbl_academic_year ay on ay.id=sub_alloc.ay_id
            left join iims_tbl_course c on c.id=sub_alloc.course_id
            left join iims_tbl_pattern p on p.id=sub_alloc.pattern_id
            left join iims_tbl_semester s on s.id=sub_alloc.sem_id
            left join iims_tbl_subjects sub on sub.id=sub_alloc.subject_id
            left join auth_user au on au.id=sub_alloc.faculty_id
            left join auth_user auc on auc.id=sub_alloc.created_by_userid
            where sub_alloc.ay_id=%s and sub_alloc.course_id=%s and sub_alloc.pattern_id=%s and 
            sub_alloc.sem_id=%s and sub_alloc.div_id=%s'''
    cur.execute(query,(ay_id,course_id,pattern_id,sem_id,div_id))
    faculty_dict = dict_build(cur)
    cur.close()
    conn.close()
    return faculty_dict

def getalldivision():
    conn = mysql.connector.connect(**db_config)
                           
    cur = conn.cursor()
    query = '''select * from iims_tbl_division'''
    cur.execute(query,)
    course_dict = dict_build(cur)
    cur.close()
    conn.close()
    return course_dict