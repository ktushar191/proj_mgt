from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
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

def save_content(**kwargs):
    content_data = kwargs
    try:
       
        conn = mysql.connector.connect(**db_config)
        cur = conn.cursor()
        query = '''insert into iims_tbl_lms_contents(content_title, course_id,pattern_id,sem_id,subject_id,chapter,content_type,content_link1,content_link2,created_datetime,created_by_userid)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''

        cur.execute(query, (content_data["content_title"], content_data["course_id"], content_data["pattern_id"],
                            content_data["sem_id"], content_data["subject_id"], content_data["chapter"], content_data["content_type"], content_data["content_link1"], content_data["content_link2"],content_data["created_datetime"],content_data["created_by_userid"]))
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

def getallstudycontent(request,inputdata):
    
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
            search += "lower(lc.content_title) LIKE '%" + search_txt.lower() + "%')"
        # print(search)
        sort_col = 'lc.created_datetime'
        sort_dir = 'DESC'
        limit_query = " LIMIT " + str(pagesize) + " OFFSET " + str(startlimit)
        if ('showall' in inputdata and inputdata['showall'] is not None and int(inputdata['showall']) == 1):
            limit_query = ""
        if 'sort_col' in inputdata and inputdata['sort_col'] != None:
            sort_col = inputdata['sort_col']
        if 'sort_dir' in inputdata and inputdata['sort_dir'] != None:
            sort_dir = inputdata['sort_dir']
        # filter = ""
        # if 'filter' in inputdata:
        #     for key in inputdata['filter']:
        #         if inputdata['filter'][key] != '':
        #             filter += " AND " + key + " = '" + inputdata['filter'][key] + "'"
       
        course_query=""
        if 'course' in inputdata and inputdata['course'] and inputdata['course'] != '':
            course_query = " AND lc.course_id = '" + str(inputdata['course']) + "' "

        pattern_query=""
        if 'pattern' in inputdata and inputdata['pattern'] and inputdata['pattern'] != '':
            pattern_query = " AND lc.pattern_id = '" + str(inputdata['pattern']) + "' "

        sem_query=""
        if 'sem' in inputdata and inputdata['sem'] and inputdata['sem'] != '':
            sem_query = " AND lc.sem_id = '" + str(inputdata['sem']) + "' "
        
        subject_query=""
        if 'subject' in inputdata and inputdata['subject'] and inputdata['subject'] != '':
            subject_query = " AND lc.subject_id = '" + str(inputdata['subject']) + "' "

   
        conn = mysql.connector.connect(**db_config)
        cur = conn.cursor()
        query = '''SELECT lc.id,lc.content_title,lc.course_id,c.course_name,lc.pattern_id,p.pattern,lc.sem_id,s.semester_name,
                    lc.subject_id,sub.subject_name,lc.chapter,lc.content_type,lc.chapter,lc.content_link1,
                    lc.content_link2,lc.created_datetime,lc.created_by_userid,au.first_name,au.last_name
                    FROM iims_db.iims_tbl_lms_contents lc 
                    left join iims_tbl_course c on lc.course_id=c.id
                    left join iims_tbl_pattern p on lc.pattern_id=p.id
                    left join iims_tbl_semester s on lc.sem_id=s.id
                    left join iims_tbl_subjects sub on lc.subject_id=sub.id
                    left join auth_user au on lc.created_by_userid=au.id
                    where true''' \
                  + course_query +pattern_query+sem_query+subject_query+ search + ''' ORDER BY ''' \
                + str(sort_col) + ''' ''' + str(sort_dir) + limit_query
       
        cur.execute(query, )
        records = dict_build(cur)
        cur.close()
        conn.close()
        # print(records)


        conn = mysql.connector.connect(**db_config)
        cur = conn.cursor()
        query1 = ''' SELECT count(lc.id)
                    FROM iims_db.iims_tbl_lms_contents lc 
                    left join iims_tbl_course c on lc.course_id=c.id
                    left join iims_tbl_pattern p on lc.pattern_id=p.id
                    left join iims_tbl_semester s on lc.sem_id=s.id
                    left join iims_tbl_subjects sub on lc.subject_id=sub.id
                    left join auth_user au on lc.created_by_userid=au.id
                    where true''' \
                 +course_query +pattern_query+sem_query+subject_query+ search
      
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
       
        return data
    except Exception as e:
        print("Exception :" + str(e))
        return None