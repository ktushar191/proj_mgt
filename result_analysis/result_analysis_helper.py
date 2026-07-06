import os
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
import mysql.connector
from django.conf import settings
import time
from helpermodule import studenthelper,commonhelper

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

def save_marks_details(**kwargs):
    try:
        #import pdb;pdb.set_trace()
        marks_data=kwargs
        conn = mysql.connector.connect(**db_config)
        cur = conn.cursor()
        query = '''insert into iims_tbl_result_student_marks(user_id, course_id, sem_id, ay_id, pattern, subject_id, ext_marks, grade_id, sgpa, status_id, marksheet_name, marksheet_url)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
        cur.execute(query,(marks_data["user_id"],marks_data["course_id"],marks_data["sem_id"],marks_data["ay_id"],marks_data["pattern"],
                    marks_data["sub_id"],marks_data["ext_marks"],marks_data["grade_id"],marks_data['sgpa'],marks_data["status_id"],marks_data["marksheet_name"],marks_data["marksheet_file_path"]))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(str(e))
        return False 
    return True

def save_assignment_marks(**kwargs):
    try:
        #import pdb;pdb.set_trace()
        assi_marks_data=kwargs
        # Use conditional expression to convert blank value to None
        assi_marks_1 = assi_marks_data.get("Assign-No 1", None) if assi_marks_data.get("Assign-No 1", None) != '' else None
        assi_marks_2 = assi_marks_data.get("Assign-No 2", None) if assi_marks_data.get("Assign-No 2", None) != '' else None
        assi_marks_3 = assi_marks_data.get("Assign-No 3", None) if assi_marks_data.get("Assign-No 3", None) != '' else None
        assi_marks_4 = assi_marks_data.get("Assign-No 4", None) if assi_marks_data.get("Assign-No 4", None) != '' else None
        assi_marks_5 = assi_marks_data.get("Assign-No 5", None) if assi_marks_data.get("Assign-No 5", None) != '' else None
        assi_marks_6 = assi_marks_data.get("Assign-No 6", None) if assi_marks_data.get("Assign-No 6", None) != '' else None
        assi_marks_7 = assi_marks_data.get("Assign-No 7", None) if assi_marks_data.get("Assign-No 7", None) != '' else None
        assi_marks_8 = assi_marks_data.get("Assign-No 8", None) if assi_marks_data.get("Assign-No 8", None) != '' else None
        assi_marks_9 = assi_marks_data.get("Assign-No 9", None) if assi_marks_data.get("Assign-No 9", None) != '' else None
        assi_marks_10 = assi_marks_data.get("Assign-No 10", None) if assi_marks_data.get("Assign-No 10", None) != '' else None
        
        conn = mysql.connector.connect(**db_config)
        cur = conn.cursor()
        query = '''insert into iims_tbl_result_analysis_assignment(user_id, course_id, sem_id, ay_id, subject_id, pattern, assi1, assi1_outof, assi2, assi2_outof, assi3, assi3_outof, assi4, assi4_outof, assi5, assi5_outof, assi6, assi6_outof,
                    assi7, assi7_outof, assi8, assi8_outof, assi9, assi9_outof, assi10, assi10_outof)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
        cur.execute(query,(assi_marks_data["user_id"],assi_marks_data["courseSelect"],assi_marks_data["semesterSelect"],assi_marks_data["aySelect"],assi_marks_data["subSelect"],assi_marks_data["patternSelect"],
                          assi_marks_1,30,assi_marks_2,30,assi_marks_3,30,assi_marks_4,30,assi_marks_5,30,
                          assi_marks_6,30,assi_marks_7,30,assi_marks_8,30,assi_marks_9,30,assi_marks_10,30))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(str(e))
        return False 
    return True

def save_mcq_marks(**kwargs):
    try:
        #import pdb;pdb.set_trace()
        mcq_marks_data=kwargs
         # Use conditional expression to convert blank value to None
        mcq_marks= mcq_marks_data.get("MCQ Test Mark's ", None) if mcq_marks_data.get("MCQ Test Mark's ", None) != '' else None
        conn = mysql.connector.connect(**db_config)
        cur = conn.cursor()
        query = '''insert into iims_tbl_result_analysis_mcq(user_id, course_id, sem_id, ay_id, subject_id, pattern, mcqmarks, mcqmarks_outof)values(%s,%s,%s,%s,%s,%s,%s,%s)'''
        cur.execute(query,(mcq_marks_data["user_id"],mcq_marks_data["courseSelect"],mcq_marks_data["semesterSelect"],mcq_marks_data["aySelect"],mcq_marks_data["subSelect"],mcq_marks_data["patternSelect"],
                           mcq_marks,30))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(str(e))
        return False 
    return True

def save_midterm_marks(**kwargs):
    try:
        #import pdb;pdb.set_trace()
        midterm_marks_data=kwargs
        # Use conditional expression to convert blank value to None
        midterm_marks= midterm_marks_data.get("Mid Term Exam Mark's ", None) if midterm_marks_data.get("Mid Term Exam Mark's ", None) != '' else None
        conn = mysql.connector.connect(**db_config)
        cur = conn.cursor()
        query = '''insert into iims_tbl_result_analysis_midterm(user_id, course_id, sem_id, ay_id, subject_id, pattern, midterm_marks, midterm_marks_outof)values(%s,%s,%s,%s,%s,%s,%s,%s)'''
        cur.execute(query,(midterm_marks_data["user_id"],midterm_marks_data["courseSelect"],midterm_marks_data["semesterSelect"],midterm_marks_data["aySelect"],midterm_marks_data["subSelect"],midterm_marks_data["patternSelect"],
                           midterm_marks,30))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(str(e))
        return False 
    return True

def save_endterm_marks(**kwargs):
    try:
        #import pdb;pdb.set_trace()
        endterm_marks_data=kwargs
        # Use conditional expression to convert blank value to None
        endterm_marks= endterm_marks_data.get("End Term Exam Mark's ", None) if endterm_marks_data.get("End Term Exam Mark's ", None) != '' else None
        conn = mysql.connector.connect(**db_config)
        cur = conn.cursor()
        query = '''insert into iims_tbl_result_analysis_endterm(user_id, course_id, sem_id, ay_id, subject_id, pattern, endterm_marks, endterm_outof)values(%s,%s,%s,%s,%s,%s,%s,%s)'''
        cur.execute(query,(endterm_marks_data["user_id"],endterm_marks_data["courseSelect"],endterm_marks_data["semesterSelect"],endterm_marks_data["aySelect"],endterm_marks_data["subSelect"],endterm_marks_data["patternSelect"],
                           endterm_marks,50))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(str(e))
        return False 
    return True

def save_subject_viva_marks(**kwargs):
    try:
        #import pdb;pdb.set_trace()
        subject_viva_marks_data=kwargs
        # Use conditional expression to convert blank value to None
        sub_viva_marks= subject_viva_marks_data.get("Subject Viva Mark's ", None) if subject_viva_marks_data.get("Subject Viva Mark's ", None) != '' else None
        conn = mysql.connector.connect(**db_config)
        cur = conn.cursor()
        query = '''insert into iims_tbl_result_analysis_subviva(user_id, course_id, sem_id, ay_id, subject_id, pattern, subviva_marks, subviva_outof)values(%s,%s,%s,%s,%s,%s,%s,%s)'''
        cur.execute(query,(subject_viva_marks_data["user_id"],subject_viva_marks_data["courseSelect"],subject_viva_marks_data["semesterSelect"],subject_viva_marks_data["aySelect"],subject_viva_marks_data["subSelect"],subject_viva_marks_data["patternSelect"],
                           sub_viva_marks,10))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(str(e))
        return False 
    return True


#22-Sep-2024
def save_open_course_marks(**kwargs):
    try:
        #import pdb;pdb.set_trace()
        academic_details=kwargs.get('academic_details',{})
        open_course_marks=kwargs.get('student_Data',{})
        # Use conditional expression to convert blank value to None
        oc_marks= open_course_marks.get("marks", None) if open_course_marks.get("marks", None) != '' else None
        conn = mysql.connector.connect(**db_config)
        cur = conn.cursor()
        query = '''insert into iims_tbl_result_analysis_open_course_marks(user_id, course_id, sem_id, ay_id, subject_id, pattern, int_marks, open_course_marks_out_of)values(%s,%s,%s,%s,%s,%s,%s,%s)'''
        cur.execute(query,(open_course_marks["user_id"],academic_details["courseSelect"],academic_details["semesterSelect"],academic_details["aySelect"],academic_details["subSelect"],academic_details["patternSelect"],
                           oc_marks,25))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(str(e))
        return False 
    return True



def save_practical_marks(**kwargs):
    try:
        #import pdb;pdb.set_trace()
        academic_details=kwargs.get('academic_details',{})
        practical_marks=kwargs.get('student_Data',{})
        # Use conditional expression to convert blank value to None
        int_practical_marks= practical_marks.get("marks", None) if practical_marks.get("marks", None) != '' else None
        ext_practical_marks= practical_marks.get("ext_marks", None) if practical_marks.get("ext_marks", None) != '' else None
        conn = mysql.connector.connect(**db_config)
        cur = conn.cursor()
        query = '''insert into iims_tbl_result_analysis_practical_marks(user_id, course_id, sem_id, ay_id, subject_id, pattern, int_marks, practical_int_marks_out_of, ext_marks, practical_ext_marks_out_of)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
        cur.execute(query,(practical_marks["user_id"],academic_details["courseSelect"],academic_details["semesterSelect"],academic_details["aySelect"],academic_details["subSelect"],academic_details["patternSelect"],
                           int_practical_marks,75,ext_practical_marks,50))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(str(e))
        return False 
    return True

def save_mini_project_marks(**kwargs):
    try:
        #import pdb;pdb.set_trace()
        academic_details=kwargs.get('academic_details',{})
        mini_project_marks=kwargs.get('student_Data',{})
        # Use conditional expression to convert blank value to None
        int_mini_project_marks= mini_project_marks.get("marks", None) if mini_project_marks.get("marks", None) != '' else None
        ext_mini_project_marks= mini_project_marks.get("ext_marks", None) if mini_project_marks.get("ext_marks", None) != '' else None
        conn = mysql.connector.connect(**db_config)
        cur = conn.cursor()
        query = '''insert into iims_tbl_result_analysis_mini_project_marks(user_id, course_id, sem_id, ay_id, subject_id, pattern, int_marks, mini_project_int_marks_out_of, ext_marks, mini_project_ext_marks_out_of)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
        cur.execute(query,(mini_project_marks["user_id"],academic_details["courseSelect"],academic_details["semesterSelect"],academic_details["aySelect"],academic_details["subSelect"],academic_details["patternSelect"],
                           int_mini_project_marks,75,ext_mini_project_marks,50))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(str(e))
        return False 
    return True


def save_major_project_marks(**kwargs):
    try:
        #import pdb;pdb.set_trace()
        academic_details=kwargs.get('academic_details',{})
        major_project_marks=kwargs.get('student_Data',{})
        # Use conditional expression to convert blank value to None
        int_major_project_marks= major_project_marks.get("marks", None) if major_project_marks.get("marks", None) != '' else None
        ext_major_project_marks= major_project_marks.get("ext_marks", None) if major_project_marks.get("ext_marks", None) != '' else None
        conn = mysql.connector.connect(**db_config)
        cur = conn.cursor()
        query = '''insert into iims_tbl_result_analysis_major_project_marks(user_id, course_id, sem_id, ay_id, subject_id, pattern, int_marks, major_project_int_marks_out_of, ext_marks, major_project_ext_marks_out_of)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
        cur.execute(query,(major_project_marks["user_id"],academic_details["courseSelect"],academic_details["semesterSelect"],academic_details["aySelect"],academic_details["subSelect"],academic_details["patternSelect"],
                           int_major_project_marks,300,ext_major_project_marks,250))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(str(e))
        return False 
    return True

def save_soft_skills_marks(**kwargs):
    try:
        #import pdb;pdb.set_trace()
        academic_details=kwargs.get('academic_details',{})
        soft_skills_marks=kwargs.get('student_Data',{})
        # Use conditional expression to convert blank value to None
        Soft_Skills_Marks= soft_skills_marks.get("marks", None) if soft_skills_marks.get("marks", None) != '' else None
        conn = mysql.connector.connect(**db_config)
        cur = conn.cursor()
        query = '''insert into iims_tbl_result_analysis_soft_skills_marks(user_id, course_id, sem_id, ay_id, subject_id, pattern, int_marks, soft_skills_marks_out_of)values(%s,%s,%s,%s,%s,%s,%s,%s)'''
        cur.execute(query,(soft_skills_marks["user_id"],academic_details["courseSelect"],academic_details["semesterSelect"],academic_details["aySelect"],academic_details["subSelect"],academic_details["patternSelect"],
                           Soft_Skills_Marks,25))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(str(e))
        return False 
    return True



#Retrive All Marks Internal and External
def getallAssignmentMarks(**kwargs):
    courseSelect=kwargs.get('course_id')
    semesterSelect=kwargs.get('sem_id')
    aySelect=kwargs.get('ay_id')
    patternSelect=kwargs.get('pattern')
    
    conn = mysql.connector.connect(**db_config)               
    cur = conn.cursor()
    query = '''select * from iims_tbl_result_analysis_assignment where course_id=%s and sem_id=%s and ay_id=%s and pattern=%s;'''
    cur.execute(query,(courseSelect,semesterSelect,aySelect,patternSelect))
    course_dict = dict_build(cur)
    cur.close()
    conn.close()
    return course_dict

def getallMCQMarks(**kwargs):
    courseSelect=kwargs.get('course_id')
    semesterSelect=kwargs.get('sem_id')
    aySelect=kwargs.get('ay_id')
    patternSelect=kwargs.get('pattern')
    
    
    conn = mysql.connector.connect(**db_config)
                           
    cur = conn.cursor()
    query = '''select * from iims_tbl_result_analysis_mcq where course_id=%s and sem_id=%s and ay_id=%s and pattern=%s;'''
    cur.execute(query,(courseSelect,semesterSelect,aySelect,patternSelect))
    course_dict = dict_build(cur)
    cur.close()
    conn.close()
    return course_dict

def getallMidTermMarks(**kwargs):
    courseSelect=kwargs.get('course_id')
    semesterSelect=kwargs.get('sem_id')
    aySelect=kwargs.get('ay_id')
    patternSelect=kwargs.get('pattern')
    
    
    conn = mysql.connector.connect(**db_config)
                           
    cur = conn.cursor()
    query = '''select * from iims_tbl_result_analysis_midterm where course_id=%s and sem_id=%s and ay_id=%s and pattern=%s;'''
    cur.execute(query,(courseSelect,semesterSelect,aySelect,patternSelect))
    course_dict = dict_build(cur)
    cur.close()
    conn.close()
    return course_dict

def getallEndTermMarks(**kwargs):
    courseSelect=kwargs.get('course_id')
    semesterSelect=kwargs.get('sem_id')
    aySelect=kwargs.get('ay_id')
    patternSelect=kwargs.get('pattern')
    
    
    conn = mysql.connector.connect(**db_config)
                           
    cur = conn.cursor()
    query = '''select * from iims_tbl_result_analysis_endterm where course_id=%s and sem_id=%s and ay_id=%s and pattern=%s;'''
    cur.execute(query,(courseSelect,semesterSelect,aySelect,patternSelect))
    course_dict = dict_build(cur)
    cur.close()
    conn.close()
    return course_dict

def getallSubjectVivaMarks(**kwargs):
    courseSelect=kwargs.get('course_id')
    semesterSelect=kwargs.get('sem_id')
    aySelect=kwargs.get('ay_id')
    patternSelect=kwargs.get('pattern')
    
    
    conn = mysql.connector.connect(**db_config)
                           
    cur = conn.cursor()
    query = '''select * from iims_tbl_result_analysis_subviva where course_id=%s and sem_id=%s and ay_id=%s and pattern=%s;'''
    cur.execute(query,(courseSelect,semesterSelect,aySelect,patternSelect))
    course_dict = dict_build(cur)
    cur.close()
    conn.close()
    return course_dict



def getallOpenCourseMarks(**kwargs):
    courseSelect=kwargs.get('course_id')
    semesterSelect=kwargs.get('sem_id')
    aySelect=kwargs.get('ay_id')
    patternSelect=kwargs.get('pattern')
    
    
    conn = mysql.connector.connect(**db_config)
                           
    cur = conn.cursor()
    query = '''select * from iims_tbl_result_analysis_open_course_marks where course_id=%s and sem_id=%s and ay_id=%s and pattern=%s;'''
    cur.execute(query,(courseSelect,semesterSelect,aySelect,patternSelect))
    course_dict = dict_build(cur)
    cur.close()
    conn.close()
    return course_dict

def getallPracticalMarks(**kwargs):
    courseSelect=kwargs.get('course_id')
    semesterSelect=kwargs.get('sem_id')
    aySelect=kwargs.get('ay_id')
    patternSelect=kwargs.get('pattern')
    
    
    conn = mysql.connector.connect(**db_config)
                           
    cur = conn.cursor()
    query = '''select * from iims_tbl_result_analysis_practical_marks where course_id=%s and sem_id=%s and ay_id=%s and pattern=%s;'''
    cur.execute(query,(courseSelect,semesterSelect,aySelect,patternSelect))
    course_dict = dict_build(cur)
    cur.close()
    conn.close()
    return course_dict

def getallMiniProjectMarks(**kwargs):
    courseSelect=kwargs.get('course_id')
    semesterSelect=kwargs.get('sem_id')
    aySelect=kwargs.get('ay_id')
    patternSelect=kwargs.get('pattern')
    
    
    conn = mysql.connector.connect(**db_config)
                           
    cur = conn.cursor()
    query = '''select * from iims_tbl_result_analysis_mini_project_marks where course_id=%s and sem_id=%s and ay_id=%s and pattern=%s;'''
    cur.execute(query,(courseSelect,semesterSelect,aySelect,patternSelect))
    course_dict = dict_build(cur)
    cur.close()
    conn.close()
    return course_dict

def getallMajorProjectMarks(**kwargs):
    courseSelect=kwargs.get('course_id')
    semesterSelect=kwargs.get('sem_id')
    aySelect=kwargs.get('ay_id')
    patternSelect=kwargs.get('pattern')
    
    
    conn = mysql.connector.connect(**db_config)
                           
    cur = conn.cursor()
    query = '''select * from iims_tbl_result_analysis_major_project_marks where course_id=%s and sem_id=%s and ay_id=%s and pattern=%s;'''
    cur.execute(query,(courseSelect,semesterSelect,aySelect,patternSelect))
    course_dict = dict_build(cur)
    cur.close()
    conn.close()
    return course_dict

def getallSoftSkillsMarks(**kwargs):
    courseSelect=kwargs.get('course_id')
    semesterSelect=kwargs.get('sem_id')
    aySelect=kwargs.get('ay_id')
    patternSelect=kwargs.get('pattern')
    
    
    conn = mysql.connector.connect(**db_config)
                           
    cur = conn.cursor()
    query = '''select * from iims_tbl_result_analysis_soft_skills_marks where course_id=%s and sem_id=%s and ay_id=%s and pattern=%s;'''
    cur.execute(query,(courseSelect,semesterSelect,aySelect,patternSelect))
    course_dict = dict_build(cur)
    cur.close()
    conn.close()
    return course_dict


def getallStudent_Subject_ExternalMarks(**kwargs):
    courseSelect=kwargs.get('course_id')
    semesterSelect=kwargs.get('sem_id')
    aySelect=kwargs.get('ay_id')
    patternSelect=kwargs.get('pattern')
    
    
    conn = mysql.connector.connect(**db_config)
                           
    cur = conn.cursor()
    query = '''select * from iims_tbl_result_student_marks where course_id=%s and sem_id=%s and ay_id=%s and pattern=%s;'''
    cur.execute(query,(courseSelect,semesterSelect,aySelect,patternSelect))
    course_dict = dict_build(cur)
    cur.close()
    conn.close()
    return course_dict


#Calculate Internal Marks of Subject
def Calculate_Internal_Marks(**kwargs):
    Internal_marks={
        'user_id':kwargs.get('user_id'),
        'course_id':kwargs.get('course_id'),
        'sem_id':kwargs.get('sem_id'),
        'ay_id':kwargs.get('ay_id'),
        'subject_id':kwargs.get('subject_id'),
        'pattern':kwargs.get('pattern'),
    }
    assi_list = ['assi1', 'assi2', 'assi3', 'assi4', 'assi5', 'assi6', 'assi7', 'assi8', 'assi9', 'assi10']
    
    # Initialize all marks and final result
    mcq_marks = kwargs.get('mcqmarks', 0)
    midterm_marks = kwargs.get('midterm_marks', 0)
    endterm_marks = kwargs.get('endterm_marks', 0)
    subviva_marks = kwargs.get('subviva_marks', 0)
    
    # Handle assignment marks
    assi_marks = [kwargs.get(assi, 0) for assi in assi_list if kwargs.get(assi) is not None]
    assi_total = sum(assi_marks)
    
    # Convert marks to the required scale
    converted_mcq_marks = mcq_marks / 3  # Conversion to 10
    converted_mid_end_term_marks = (midterm_marks + endterm_marks) / 16  # Conversion to 5
    converted_sub_viva_marks = subviva_marks / 2  # Conversion to 5
    converted_assi_marks = assi_total / (30 * len(assi_marks) / 5) if assi_marks else 0
    
    # Final internal marks calculation
    Final_internal_marks = (
        converted_mcq_marks +
        converted_mid_end_term_marks +
        converted_sub_viva_marks +
        converted_assi_marks
    )
    
    Internal_marks["int_marks"]=round(Final_internal_marks)
    return Internal_marks


def getallteachers_details():
    conn = mysql.connector.connect(**db_config)
                           
    cur = conn.cursor()
    query = '''select * from iims_db.user_profiles where user_type="f";'''
    cur.execute(query,)
    all_student_data_dict = dict_build(cur)
    cur.close()
    conn.close()
    return all_student_data_dict

def getfaculty_subject_mapping(subject_id,ay_id,course_id,pattern_id,sem_id):
    conn = mysql.connector.connect(**db_config)
                           
    cur = conn.cursor()
    query = '''select faculty_id,subject_id from iims_db.iims_tbl_subject_allocation where subject_id=%s and ay_id=%s and course_id=%s and pattern_id=%s and sem_id=%s ;'''
    cur.execute(query,(subject_id,ay_id,course_id,pattern_id,sem_id))
    faculty_subject_mapping = dict_build(cur)
    cur.close()
    conn.close()
    return faculty_subject_mapping      
        
    

#get id when pass grade_name and get grade_name when pass id
def get_grade_info(key, value):
    al_grade =commonhelper.getallgrade()
    for grade in al_grade:
        if grade[key] == value:
            return grade['id'] if key == 'grade_name' else grade['grade_name']
    return None

def get_pattern_id(pattern):
    pattern_data =commonhelper.getallpatterns()
    # Iterate over the list of dictionaries
    for entry in pattern_data:
        if entry['pattern'] == pattern:
            return entry['id']
    return None  # Return None if pattern is not found