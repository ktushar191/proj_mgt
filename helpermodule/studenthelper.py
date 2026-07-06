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

def getallroles():

    db_config = {
    "host": settings.DB_CREDENTIALS['HOST'],
    "user": settings.DB_CREDENTIALS['USER'],
    "password": settings.DB_CREDENTIALS['PASSWORD'],
    "database": settings.DB_CREDENTIALS['NAME']
    }
    conn = mysql.connector.connect(**db_config)
                           
    cur = conn.cursor()
    query = '''select * from user_role'''
    cur.execute(query,)
    user_role = dict_build(cur)
    cur.close()
    conn.close()
    return user_role

def save_userprofile(**kwargs):
    try:
        
        user_data=kwargs
        field_mapping={
            "userid":"user_id",
            "firstname":"first_name",
            "lastname":"last_name",
            "email":"email",
            "mobile":"mobile",
            "user_type":"user_type",
            "isemailverified":"is_email_verified",
            "ismobileverified":"is_mobile_verified"
        }
        default_values={
            "userid":"",
            "firstname":"",
            "lastname":"",
            "email":"",
            "mobile":"",
            "user_type":"",
            "isemailverified":False,
            "ismobileverified":False
        }
        user_info={}
        for key,value in field_mapping.items():
            if user_data.get(key):
                user_info.update({value:user_data[key]})
            else:
                user_info.update({value:default_values[key]})
        conn = mysql.connector.connect(**db_config)
                            
        cur = conn.cursor()
        query = '''insert into user_profiles(user_id,first_name,last_name,email,mobile,user_type,is_email_verified,is_mobile_verified)values(%s,%s,%s,%s,%s,%s,%s,%s)'''
      
        cur.execute(query,(user_info["user_id"],user_info["first_name"],user_info["last_name"],user_info["email"],
                        user_info["mobile"],user_info["user_type"],user_info["is_email_verified"],user_info["is_mobile_verified"]))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(str(e))
        return False 
    return True
    
def is_mobile_exist(mobile):
    db_config = {
    "host": settings.DB_CREDENTIALS['HOST'],
    "user": settings.DB_CREDENTIALS['USER'],
    "password": settings.DB_CREDENTIALS['PASSWORD'],
    "database": settings.DB_CREDENTIALS['NAME']
    }
    conn = mysql.connector.connect(**db_config)
    cur = conn.cursor()
    query = '''select * from user_profiles where mobile= %s'''
    cur.execute(query,(mobile,))
    mobile_data = dict_build(cur)
    cur.close()
    conn.close()
    return mobile_data

def is_email_exist(email):
    db_config = {
    "host": settings.DB_CREDENTIALS['HOST'],
    "user": settings.DB_CREDENTIALS['USER'],
    "password": settings.DB_CREDENTIALS['PASSWORD'],
    "database": settings.DB_CREDENTIALS['NAME']
    }
    conn = mysql.connector.connect(**db_config)
    cur = conn.cursor()
    query = '''select * from auth_user where email= %s'''
    cur.execute(query,(email,))
    mobile_data = dict_build(cur)
    cur.close()
    conn.close()
    return mobile_data

def is_username_exist(username):
    db_config = {
    "host": settings.DB_CREDENTIALS['HOST'],
    "user": settings.DB_CREDENTIALS['USER'],
    "password": settings.DB_CREDENTIALS['PASSWORD'],
    "database": settings.DB_CREDENTIALS['NAME']
    }
    conn = mysql.connector.connect(**db_config)
    cur = conn.cursor()
    query = '''select * from auth_user where username= %s'''
    cur.execute(query,(username,))
    mobile_data = dict_build(cur)
    cur.close()
    conn.close()
    return mobile_data

def save_academic_details(**kwargs):
    
    try:
        user_data=kwargs
        field_mapping={
            "user_id":"user_id",
            "course_id":"course_id",
            "ay_year_id":"ay_year_id",
            "admission_through_id":"admission_through_id",
            "category_id":"category_id",
            "previous_qualification":"previous_qualification",
            "previous_qualification_perc":"previous_qualification_perc",
            "is_academic_data_exist":"is_academic_data_exist",
            "roll_no":"roll_no",
            "division":"division",
            "current_semester":"current_semester"

          
        }
        default_values={
            "user_id":"",
            "course_id":"",
            "ay_year_id":"",
            "admission_through_id":"",
            "category_id":"",
            "previous_qualification":"",
            "previous_qualification_perc":"",
            "is_academic_data_exist":False,
            "roll_no":"",
            "division":"",
            "current_semester":""
        }
        user_academic_info={}
        for key,value in field_mapping.items():
            if user_data.get(key):
                user_academic_info.update({value:user_data[key]})
            else:
                user_academic_info.update({value:default_values[key]})

        conn = mysql.connector.connect(**db_config)
        cur = conn.cursor()
        if not user_academic_info['is_academic_data_exist']:

            query = '''insert into iims_tbl_user_academic_details(user_id,course_id,ay_year_id,admission_through_id,category_id,previous_qualification,previous_qualification_perc,roll_no,division_id,current_semester_id)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
            cur.execute(query,(user_academic_info["user_id"],user_academic_info["course_id"],user_academic_info["ay_year_id"],user_academic_info["admission_through_id"],
                        user_academic_info["category_id"],user_academic_info["previous_qualification"],user_academic_info["previous_qualification_perc"],user_academic_info["roll_no"],user_academic_info["division"],user_academic_info["current_semester"]))
        else:
            query= '''update iims_tbl_user_academic_details set course_id=%s,ay_year_id=%s,admission_through_id=%s,category_id=%s,previous_qualification=%s,previous_qualification_perc=%s ,roll_no=%s,division_id=%s,current_semester_id=%s where user_id=%s'''
            cur.execute(query,(user_academic_info["course_id"],user_academic_info["ay_year_id"],user_academic_info["admission_through_id"],
                        user_academic_info["category_id"],user_academic_info["previous_qualification"],user_academic_info["previous_qualification_perc"],user_academic_info["roll_no"],user_academic_info["division"],user_academic_info["current_semester"],user_academic_info["user_id"]))
        
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(str(e))
        return False 
    return True

def updateprofileimages(images,user_id):
    try:
    
        db_config = {
        "host": settings.DB_CREDENTIALS['HOST'],
        "user": settings.DB_CREDENTIALS['USER'],
        "password": settings.DB_CREDENTIALS['PASSWORD'],
        "database": settings.DB_CREDENTIALS['NAME']
        }
        conn = mysql.connector.connect(**db_config)
        cur = conn.cursor()
        query = '''update user_profiles set image_main_url=%s,image_bigthumb_url=%s,image_smallthumb_url=%s where user_id=%s'''
        cur.execute(query,(images['image_main_url'],images['image_bigthumb_url'],images['image_smallthumb_url'],user_id))
        
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(str(e))
        return False 
    return True

def get_academic_details_by_user_id(user_id):
    try:
        academic_data=None
        db_config = {
        "host": settings.DB_CREDENTIALS['HOST'],
        "user": settings.DB_CREDENTIALS['USER'],
        "password": settings.DB_CREDENTIALS['PASSWORD'],
        "database": settings.DB_CREDENTIALS['NAME']
        }
        conn = mysql.connector.connect(**db_config)
        cur = conn.cursor()
        query = '''select * from iims_tbl_user_academic_details where user_id= %s'''
        cur.execute(query,(user_id,))
        academic_data = dict_build(cur)
        cur.close()
        conn.close()
        
    except Exception as e:
        print(str(e))
        
    return academic_data


def get_family_details_by_user_id(user_id):
    try:
        family_data=None
        db_config = {
        "host": settings.DB_CREDENTIALS['HOST'],
        "user": settings.DB_CREDENTIALS['USER'],
        "password": settings.DB_CREDENTIALS['PASSWORD'],
        "database": settings.DB_CREDENTIALS['NAME']
        }
        conn = mysql.connector.connect(**db_config)
        cur = conn.cursor()
        query = '''select * from iims_tbl_user_family_details where user_id= %s'''
        cur.execute(query,(user_id,))
        family_data = dict_build(cur)
        cur.close()
        conn.close()
        
    except Exception as e:
        print(str(e))
        
    return family_data


def save_family_details(**kwargs):
    
    try:
        
        user_data=kwargs
        field_mapping={
            "user_id":"user_id",
            "fathername":"fathername",
            "mothername":"mothername",
            # "no_of_siblings":"no_of_siblings",
            # "father_occupation":"father_occupation",
            "address1":"address1",
            "address2":"address2",
            "address3":"address3",
            "country":"country",
            "state":"state",
            "district":"district",
            "pin":"pin",
            "is_family_data_exist":"is_family_data_exist",
            "is_address_data_exist":"is_address_data_exist"
          
        }
        default_values={
            "user_id":"",
            "fathername":"",
            "mothername":"",
            # "no_of_siblings":"",
            # "father_occupation":"",
            "address1":"",
            "address2":"",
            "address3":"",
            "country":"",
            "state":"",
            "district":"",
            "pin":"",
            "is_family_data_exist":False,
            "is_address_data_exist":False
        }
        user_family_info={}
        for key,value in field_mapping.items():
            if user_data.get(key):
                user_family_info.update({value:user_data[key]})
            else:
                user_family_info.update({value:default_values[key]})

       
        conn = mysql.connector.connect(**db_config)
        cur = conn.cursor()
        if not user_family_info['is_family_data_exist']:

            query = '''insert into iims_tbl_user_family_details(user_id,father_name,mother_name)values(%s,%s,%s)'''
            cur.execute(query,(user_family_info["user_id"],user_family_info["fathername"], user_family_info["mothername"]))
                       
        else:
            query= '''update iims_tbl_user_family_details set father_name=%s,mother_name=%s where user_id=%s'''
            cur.execute(query,(user_family_info["fathername"],user_family_info["mothername"],user_family_info["user_id"]))
        
        conn.commit()
        cur.close()
        conn.close()



    except Exception as e:
        print(str(e))
        return False 
    return True


def getallstudentslist(request,inputdata):
    
    global min_date, max_date
    try:
        
        totalcount = startitem = enditem = pagecount = 0
        pagesize = inputdata['pagesize']
        startlimit = (inputdata['currentpage'] - 1) * pagesize
        # currentpage = inputdata['currentpage']
        search_txt = ''
        if 'search' in inputdata and inputdata['search'] and inputdata['search'] != '':
            search_txt = inputdata['search']

        search = ''
        if search_txt != '':
            search = " AND ("
            search += "lower(au.first_name) LIKE '%" + search_txt.lower() + "%' OR lower(au.last_name) LIKE '%" + \
                        search_txt.lower() + "%')"
        # print(search)
        sort_col = 'au.first_name'
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
            course_query = " AND user_details.course_id = '" + str(inputdata['course']) + "' "
        
        batch_query = ''
        if 'batch' in inputdata and inputdata['batch'] and inputdata['batch'] != '':
            batch_query = " AND user_details.batch= '"+ str(inputdata['batch']) + "' "

        semester_query=""
        if 'semester' in inputdata and inputdata['semester'] and inputdata['semester'] != '':
            semester_query = " AND user_details.current_semester_id = '" + str(inputdata['semester']) + "' "   

   
        conn = mysql.connector.connect(**db_config)
        cur = conn.cursor()
        query = '''select au.id,au.username,au.first_name,au.last_name,au.email,au.is_superuser,au.is_staff,au.is_active,
                    au.date_joined,au.last_login,up.mobile,up.user_type,up.is_mobile_verified,up.is_email_verified ,
                    up.image_main_url,up.image_bigthumb_url,up.image_smallthumb_url,
                    user_details.*,ufd.father_name,ufd.mother_name,ufd.no_of_siblings,ufd.fathers_occupation,user_details.batch_name
                    from auth_user au left join user_profiles up on au.id=up.user_id and au.is_active=1 and up.user_type='s'
                    left join (select uad.user_id,uad.course_id,itc.course_name,itc.course_fees,uad.ay_year_id,ay.ayear,uad.admission_through_id,
                    adt.admission_under_name,uad.category_id,c.category,uad.previous_qualification,uad.previous_qualification_perc,
                    uad.division_id,uad.current_semester_id,d.div_name,se.semester_name,uad.batch,cb.batch_name
                    from iims_tbl_user_academic_details uad left join iims_tbl_course itc on uad.course_id=itc.id
                    left join iims_tbl_academic_year ay on uad.ay_year_id=ay.id
                    left join iims_tbl_admission_through adt on uad.admission_through_id=adt.id               
                    left join iims_tbl_category c on uad.category_id=c.id
                    left join iims_tbl_division d on uad.division_id=d.id 
                    left join iims_tbl_course_batch cb on uad.batch=cb.id
                    left join iims_tbl_semester se on uad.current_semester_id=se.id) as user_details on au.id=user_details.user_id
                    left join iims_tbl_user_family_details ufd on au.id=ufd.user_id where true''' \
                +course_query +batch_query +semester_query+ search + ''' ORDER BY ''' \
                + str(sort_col) + ''' ''' + str(sort_dir) + limit_query
       
        cur.execute(query, )
        records = dict_build(cur)
        cur.close()
        conn.close()
        # print(records)


        conn = mysql.connector.connect(**db_config)
        cur = conn.cursor()
        query1 = ''' select count(au.id)
                        from auth_user au left join user_profiles up on au.id=up.user_id and au.is_active=1 and up.user_type='s'
                    left join (select uad.user_id,uad.course_id,itc.course_name,itc.course_fees,uad.ay_year_id,ay.ayear,uad.admission_through_id,
                    adt.admission_under_name,uad.category_id,c.category,uad.previous_qualification,uad.previous_qualification_perc,
                    uad.division_id,uad.current_semester_id,d.div_name,se.semester_name,uad.batch,cb.batch_name
                    from iims_tbl_user_academic_details uad left join iims_tbl_course itc on uad.course_id=itc.id
                    left join iims_tbl_academic_year ay on uad.ay_year_id=ay.id
                    left join iims_tbl_admission_through adt on uad.admission_through_id=adt.id               
                    left join iims_tbl_category c on uad.category_id=c.id
                    left join iims_tbl_division d on uad.division_id=d.id 
                    left join iims_tbl_course_batch cb on uad.batch=cb.id
                    left join iims_tbl_semester se on uad.current_semester_id=se.id) as user_details on au.id=user_details.user_id
                    left join iims_tbl_user_family_details ufd on au.id=ufd.user_id where true''' \
                        +course_query +batch_query +semester_query+ search 
        
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


def getfeedbackdata(audience_id):
    try:
        
        conn = mysql.connector.connect(**db_config)                
        cur = conn.cursor()
        query = '''select fb.* , ft.feedback_for,ft.feedback_for_shortname ,fa.audience,ay.ayear,up.first_name,up.last_name
                    from iims_tbl_feedback fb 
                    left join iims_tbl_feedback_type ft on fb.feedback_type_id=ft.id
                    left join iims_tbl_feedback_audience fa on fb.audience_id=fa.id
                    left join iims_tbl_academic_year ay on fb.a_year_id= ay.id
                    left join user_profiles up on fb.created_by_userid=up.user_id 
                    WHERE now() <= cast(concat(end_date, ' ', end_time) as datetime)
                    and (fb.audience_id =%s or fa.audience='All')'''
        cur.execute(query,(audience_id,))
        feedback_dict = dict_build(cur)
        cur.close()
        conn.close()
        return feedback_dict
    except Exception as e:
        return None


def get_address_details_by_user_id(user_id):
    try:
        address_data=None
        db_config = {
        "host": settings.DB_CREDENTIALS['HOST'],
        "user": settings.DB_CREDENTIALS['USER'],
        "password": settings.DB_CREDENTIALS['PASSWORD'],
        "database": settings.DB_CREDENTIALS['NAME']
        }
        conn = mysql.connector.connect(**db_config)
        cur = conn.cursor()
        query = '''select * from iims_tbl_user_address where user_id= %s'''
        cur.execute(query,(user_id,))
        address_data = dict_build(cur)
        cur.close()
        conn.close()
        
    except Exception as e:
        print(str(e))
        
    return address_data


def save_address_details(**kwargs):
    
    try:
       
        user_data=kwargs
        field_mapping={
            "user_id":"user_id",
            "fathername":"fathername",
            "mothername":"mothername",
            # "no_of_siblings":"no_of_siblings",
            # "father_occupation":"father_occupation",
            "address1":"address1",
            "address2":"address2",
            "address3":"address3",
            "country":"country",
            "state":"state",
            "district":"district",
            "pin":"pin",
            "is_family_data_exist":"is_family_data_exist",
            "is_address_data_exist":"is_address_data_exist"
          
        }
        default_values={
            "user_id":"",
            "fathername":"",
            "mothername":"",
            # "no_of_siblings":"",
            # "father_occupation":"",
            "address1":"",
            "address2":"",
            "address3":"",
            "country":"",
            "state":"",
            "district":"",
            "pin":"",
            "is_family_data_exist":False,
            "is_address_data_exist":False
        }
        user_address_info={}
        for key,value in field_mapping.items():
            if user_data.get(key):
                user_address_info.update({value:user_data[key]})
            else:
                user_address_info.update({value:default_values[key]})

       
        conn = mysql.connector.connect(**db_config)
        cur = conn.cursor()
        if not user_address_info['is_address_data_exist']:

            query = '''insert into iims_tbl_user_address(user_id,address_line_1,address_line_2,address_line_3,country,state,district,pin)values(%s,%s,%s,%s,%s,%s,%s,%s)'''
            cur.execute(query,(user_address_info["user_id"],user_address_info["address1"],user_address_info["address2"],user_address_info["address3"],
            user_address_info["country"],user_address_info["state"],user_address_info["district"],user_address_info["pin"]))
                        
        else:
            query= '''update iims_tbl_user_address set address_line_1=%s,address_line_2=%s, address_line_3=%s, country=%s,state=%s,district=%s,pin=%s where user_id=%s'''
            cur.execute(query,(user_address_info["address1"],user_address_info["address2"],user_address_info["address3"],
            user_address_info["country"],user_address_info["state"],user_address_info["district"],user_address_info["pin"],user_address_info["user_id"]))
        
        conn.commit()
        cur.close()
        conn.close()



    except Exception as e:
        print(str(e))
        return False 
    return True