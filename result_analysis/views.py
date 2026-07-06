import json
import os
import time
from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect, JsonResponse
from django.contrib import messages

from django.contrib.auth.decorators import login_required

from helpermodule import studenthelper,commonhelper
from django.template import Context

from .models import *
from django.contrib.auth import authenticate, login, logout
from . import result_analysis_helper
import pandas as pd
from collections import defaultdict #to handle initialized any dictionary with 0 without knowing keys
#Student Module
def result_form(request):
    context={}
    context=commonhelper.get_login_user_common_context(request.user,context)
    
    if request.method=="GET":
        course_details=commonhelper.getallcourse()
        semester_details=commonhelper.getallsemester()
        subject_details=json.dumps(commonhelper.getallsubjects())#Make None to Null
        acedemic_year=commonhelper.getallacademicyear()
        grade_details=commonhelper.getallgrade()
        pattern=commonhelper.getallpatterns()
        context['course_details']=course_details
        context['semester_details']=semester_details
        context['subject_details']=subject_details
        context['acedemic_year']=acedemic_year
        context['grade_details']=grade_details
        context['pattern']=pattern
        return render(request,"student/add_marks.html",context)
    
    if request.method=="POST":
        status=False
        table_data=request.POST.get('table_data','')
        
        try:
        # Parse the JSON string into a Python list
            table_data = json.loads(table_data)
            if 'marksheet_input' in request.FILES:
                posted_file=request.FILES['marksheet_input']
                        # Specify the directory where the files will be saved
                upload_dir = 'static/result_analysis/images/Marksheet/'
               
                
                # Ensure the directory exists
                if not os.path.exists(upload_dir):
                    os.makedirs(upload_dir)
                # Generate a unique file name
                file_name = posted_file.name
                extension = file_name.split('.')[-1]
                unique_file_name = f"{context['user_profile'][0]['username']}_Marksheet_{int(time.time())}.{extension}"
                file_path = os.path.join(upload_dir, unique_file_name)
                # Save the file to the specified directory
                with open(file_path, 'wb+') as destination:
                    for chunk in posted_file.chunks():
                        destination.write(chunk)
                        
                for i in range(len(table_data)):
                    sgpa=None
                    if table_data[i][7] !="":
                        sgpa=table_data[i][7]
                    marks_details={
                        "user_id":context['user_profile'][0]['id'],
                        "username":context['user_profile'][0]['username'], 
                        "course_id":int(table_data[i][0]),
                        "sem_id":int(table_data[i][1]),
                        "ay_id":int(table_data[i][2]),
                        "pattern":int(table_data[i][3]),
                        "sub_id":int(table_data[i][4]),
                        "ext_marks":int(table_data[i][5]),
                        "grade_id":int(table_data[i][6]),
                        "sgpa":sgpa,
                        "status_id":int(table_data[i][8]),
                        "marksheet_name":unique_file_name,
                        "marksheet_file_path":file_path
                    }
                    status=result_analysis_helper.save_marks_details(**marks_details)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid data'})
        except Exception as ex:
            return JsonResponse({'status': 'error', 'message': 'Failed to upload marksheet.'})
        if status:
            return JsonResponse({'status':'success','message':'Response recorded successfully'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Something went wrong'})
        


#**********************************************************************************

#Faculty Module
def faculty_dashboard(request):
    context={}
    context=commonhelper.get_login_user_common_context(request.user,context)
    if request.method=="GET":
       
        return render(request,"faculty/faculty_dashboard.html",context)
    
def Insert_Data(table_name,**kwargs):
    Internal_marks={}
    all_statuses = []
    academic_details=kwargs.get('academic_details',{})
    table_data=kwargs.get('table_data',{})
    for user_id,data in table_data.items():
        Internal_marks['user_id']=user_id
        for assi_list in data:
            for assi_name,assi_marks in assi_list.items():
                Internal_marks[assi_name]=assi_marks
        Internal_marks.update(academic_details) 
        match table_name:
            case 'assignmentTable':
                status=result_analysis_helper.save_assignment_marks(**Internal_marks)
            case 'mcqTable':
                status=result_analysis_helper.save_mcq_marks(**Internal_marks)
            case 'midTermTable':
                status=result_analysis_helper.save_midterm_marks(**Internal_marks)
            case 'endTermTable':
                status=result_analysis_helper.save_endterm_marks(**Internal_marks)
            case 'vivaTable':
                status=result_analysis_helper.save_subject_viva_marks(**Internal_marks)
        all_statuses.append(status)
     # Determine overall status based on all insertion results
    overall_status = all(status for status in all_statuses)
    return overall_status 
                    
          
        
def faculty_internal_marks(request):
    context={}
    context=commonhelper.get_login_user_common_context(request.user,context)
    course_and_ay_id_details=[]
    if request.method=="GET":
        
        student_data=commonhelper.getallstudent_details()
        for stud_data in student_data:
            course_and_ay_id_details.extend(commonhelper.get_course_id_ay_id_by_userid((stud_data['user_id'],)))
      
        course_details=commonhelper.getallcourse()
        semester_details=commonhelper.getallsemester()
        subject_details=json.dumps(commonhelper.getallsubjects()) #Make None to Null
        acedemic_year=commonhelper.getallacademicyear()
        pattern=commonhelper.getallpatterns()
        context['course_details']=course_details
        context['semester_details']=semester_details
        context['subject_details']=subject_details
        context['acedemic_year']=acedemic_year
        context['pattern']=pattern
        context['student_data']=json.dumps(student_data or {}) #json.dumps for handling null values
        context['course_and_ay_id_details']=json.dumps(course_and_ay_id_details or {})
        return render(request,"faculty/faculty_Internal_marks.html",context)

    if request.method=="POST":
        status=False
        Response_message=""
        clicked_button=request.POST.get('clickedButton')
        all_status=[]
        studentData=request.POST.get('studentData','')
        try:
            # Parse the JSON string into a Python list
            student_Data = json.loads(studentData)
            academic_details={
                    'courseSelect':student_Data.pop('courseSelect'),
                    'semesterSelect':student_Data.pop('semesterSelect'),
                    'aySelect':student_Data.pop('aySelect'),
                    'subSelect':student_Data.pop('subSelect'),
                    'patternSelect':student_Data.pop('patternSelect')
                }
            
            if clicked_button=="sub-marks-btn":    
                for table_name,table_data in student_Data.items():
                    query_status=Insert_Data(table_name,academic_details=academic_details,table_data=table_data)
                    all_status.append(query_status)
                    
                status=all(all_status)#Determine the overall status every element is true
                Response_message="Student's Internal Marks have been recorded successfully!"
            else:
                table_id=student_Data.pop('table_id')
                for key,data in student_Data.items():
                    tbl_data={
                        "user_id":key,
                        "marks":list(data[0].values())[0]
                    }
                    match table_id:  
                        case 'open_course_Table':
                            status=result_analysis_helper.save_open_course_marks(student_Data=tbl_data,academic_details=academic_details)
                            Response_message="Student's Open Course Marks have been recorded successfully!"
                        case 'practical_Marks_Table':
                            tbl_data["ext_marks"]=list(data[1].values())[0]
                            status=result_analysis_helper.save_practical_marks(student_Data=tbl_data,academic_details=academic_details)
                            Response_message="Student's Practical Marks have been recorded successfully!"
                        case 'mini_project_Table':
                            tbl_data["ext_marks"]=list(data[1].values())[0]
                            status=result_analysis_helper.save_mini_project_marks(student_Data=tbl_data,academic_details=academic_details)
                            Response_message="Student's Mini Project Marks have been recorded successfully!"
                        case 'major_project_Table':
                            tbl_data["ext_marks"]=list(data[1].values())[0]
                            status=result_analysis_helper.save_major_project_marks(student_Data=tbl_data,academic_details=academic_details)
                            Response_message="Student's Major Project Marks have been recorded successfully!"
                        case 'soft_skills_Table':
                            status=result_analysis_helper.save_soft_skills_marks(student_Data=tbl_data,academic_details=academic_details)
                            Response_message="Student's Soft Skills Marks have been recorded successfully!"
                        
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': "Failed to record Student's Internal Marks. Please try again or contact support."})
        if status:
            return JsonResponse({'status':'success','message':Response_message})
        else:
            return JsonResponse({'status': 'error', 'message': "Failed to record Student's Internal Marks. Please try again or contact support."})
            
            
          
#Combine List in one Dictionaries
def CombineListInDict(all_lists):
     # Initialize a dictionary to hold the merged results
        merged_dict = {}

        # Iterate through each list of dictionaries
        for data_list in all_lists:
            for item in data_list:
                # Create a unique key based on the identifiers
                key = (item['user_id'], item['course_id'], item['sem_id'], item['ay_id'], item['subject_id'], item['pattern'])
                
                # If the key doesn't exist in merged_dict, create a new entry
                if key not in merged_dict:
                    merged_dict[key] = {k: v for k, v in item.items() if k not in ['id']}
                else:
                    # If the key exists, update the dictionary with new values
                    merged_dict[key].update({k: v for k, v in item.items() if k not in ['id']})

        # Convert merged_dict back to a list of dictionaries if needed
        final_result = [dict(v) for v in merged_dict.values()]
        return final_result

def combined_marks(data):
    print(data)
    # Dictionary to store the combined result
    result = {}
    
    # Loop through each record
    for record in data:
        # Create a unique key combining user_id, course_id, sem_id, and ay_id
        key = (record['user_id'], record['course_id'], record['sem_id'], record['ay_id'])
        
        # If this combination is not in the result, initialize it
        if key not in result:
            result[key] = {
                'user_id': record['user_id'],
                'course_id': record['course_id'],
                'sem_id': record['sem_id'],
                'ay_id': record['ay_id'],
                'pattern': record['pattern'],
                'subjects': {}
            }
        
        # Add subject data into the subjects dictionary and handle None in sgpa
        subject_id = record['subject_id']
        result[key]['subjects'][subject_id] = {
            k: (v if k != 'sgpa' else (v if v is not None else 'N/A')) for k, v in record.items()
            if k not in ['user_id', 'course_id', 'sem_id', 'ay_id', 'pattern']
        }
        if 'sgpa' in record:
            result[key]['sgpa']=record['sgpa'] if record['sgpa'] is not None else 'N/A'
        if 'marksheet_url' in record:
            result[key]['marksheet_url']=record['marksheet_url'] if record['marksheet_url'] is not None else '#'
         
    # Convert result into a list format if required
    final_output = list(result.values())
    return final_output

#Assign Grade id to grade of Open Course and SoftSkills
def assign_grade_id(data, ID_OC_SoftSkills):
   
    # Grade ranges
    grade_ranges = [
        (25, 23, result_analysis_helper.get_grade_info('grade_name','O')),  # 23-25 marks -> O
        (22, 20, result_analysis_helper.get_grade_info('grade_name','A')),  # 20-22 marks -> A
        (19, 17, result_analysis_helper.get_grade_info('grade_name','B')),  # 17-19 marks -> B
        (16, 15, result_analysis_helper.get_grade_info('grade_name','C')),  # 15-16 marks -> C
        (14, 13, result_analysis_helper.get_grade_info('grade_name','D')),  # 13-14 marks -> D
        (12, 10, result_analysis_helper.get_grade_info('grade_name','E')),  # 10-12 marks -> E
        (9, 0, result_analysis_helper.get_grade_info('grade_name','F')),    # <10 marks -> F
        (0,0,result_analysis_helper.get_grade_info('grade_name','AP'))       #Absent
    ]
   
    for user_data in data:
        for subject_id, subject_info in user_data['subjects'].items():
            # Check if subject is in the specified Open Course and Soft Skills IDs
            if subject_id in ID_OC_SoftSkills:
                tot_marks = subject_info.get('tot_marks', 0)
                
                # Determine the grade_id based on marks range
                grade_id = None
                for upper, lower, gid in grade_ranges:
                    if lower <= tot_marks <= upper:
                        grade_id = gid
                        break
               
                # Update the grade_id in the subject info
                subject_info['grade_id'] = grade_id
                if grade_id ==7 or grade_id ==9:
                    subject_info['status_id']=2
                else:
                    subject_info['status_id']=1
                    
    return data


#Analysis_Table Format  
def get_user_full_names(student_data, user_ids):
    # Create a dictionary to map user IDs to full names from the student_data
    user_full_names = {
        user['user_id']: f"{user['first_name']} {user['last_name']}"
        for user in student_data if str(user['user_id']) in map(str, user_ids)
    }
    return user_full_names

#Check ATKT Subject
def process_user_marks(marks_data,subject_details):

    # Create a mapping from subject ID to subject short name for quick lookup
    subject_id_to_short_name = {subject['id']: subject['subject_short_name'] for subject in subject_details}
    # Loop through each user record
    for user in marks_data:
        subjects = user['subjects']
        status_ids = {sub_id: sub_info['status_id'] for sub_id, sub_info in subjects.items() if 'status_id' in sub_info}
          # Extract status_id for each subject
        
        # Check conditions for pass, fail, and fail with ATKT
        all_pass = all(status == 1 for status in status_ids.values())  # All status_id == 1
        all_fail = all(status != 1 for status in status_ids.values())  # All status_id != 1
        # Match sub_id to subject details and get the subject_short_name for failed subjects
        failed_subjects = [subject_id_to_short_name.get(sub_id, 'Unknown Subject') for sub_id, status in status_ids.items() if status != 1]

        if all_pass:
            # If all subjects are passed
            user['status'] = 'Pass'
            user['failed_subjects'] = "N/A"
        elif all_fail:
            # If all subjects are failed
            user['status'] = 'Fail'
            user['failed_subjects'] = "All"  # Add the failed subjects with their status_id
        else:
            # If some subjects are passed and some are failed
            user['status'] = 'Fail with ATKT'
            user['failed_subjects'] = failed_subjects  # Add the failed subjects with their status_id

    return marks_data

#Calculating Grade Count
def Calculate_Grade_Count(marks_data):
  # Initialize the grade count dictionary
    grade_count_dict = {}

    # Loop through each user record
    for user in marks_data:
        subjects = user['subjects']
        
        # Loop through each subject
        for sub_id, sub_info in subjects.items():
            grade_id = sub_info.get('grade_id')
            
            if grade_id is not None:  # Check if grade_id exists
                if sub_id not in grade_count_dict:
                    grade_count_dict[sub_id] = {result_analysis_helper.get_grade_info('grade_name','O'):0,
                                                result_analysis_helper.get_grade_info('grade_name','A'):0,
                                                result_analysis_helper.get_grade_info('grade_name','B'):0,
                                                result_analysis_helper.get_grade_info('grade_name','C'):0,
                                                result_analysis_helper.get_grade_info('grade_name','D'):0,
                                                result_analysis_helper.get_grade_info('grade_name','E'):0,
                                                result_analysis_helper.get_grade_info('grade_name','F'):0,
                                                result_analysis_helper.get_grade_info('grade_name','AP'):0,
                                                "Total":0}  # Initialize inner dictionary if sub_id not present
                grade_count_dict[sub_id][grade_id] += 1  # Increment count for the grade_id
                # Increment the total count for the subject
                grade_count_dict[sub_id]["Total"] += 1

    return grade_count_dict
        
#Subject-wise Student Performance Summary
def Subject_wise_Student_Performance(filtered_subjects, ay_id,course_id,pattern_id,sem_id,marks_data):
    #Calcuating subject performance
    subject_performance = {}
    # Iterate over each student's marks data
    for student in marks_data:
        subjects = student['subjects']
        # Iterate over each subject in the student's record
        for subject_id, subject_data in subjects.items():
            # Initialize subject stats if not already present
            if subject_id not in subject_performance:
                subject_performance[subject_id] = {
                    'students_appeared': 0,
                    'students_passed': 0,
                    'students_failed': 0,
                    'students_absent': 0,
                    'pass_percentage': 0.0
                }
                # Check if the student is absent based on grade_id == 9
            if 'grade_id' in subject_data and subject_data['grade_id'] == result_analysis_helper.get_grade_info('grade_name','AP'):
                subject_performance[subject_id]['students_absent'] += 1
            else:
                # If grade_id is not 9, check if the student appeared (has ext_marks)
                if 'tot_marks' in subject_data and subject_data['tot_marks'] is not None:
                    subject_performance[subject_id]['students_appeared'] += 1

                    # Check if the student passed the subject (assuming status_id == 1 is "Pass")
                    if 'status_id' in subject_data and subject_data['status_id'] == 1:
                        subject_performance[subject_id]['students_passed'] += 1
                    else:
                        subject_performance[subject_id]['students_failed'] += 1

    # Calculate pass percentage for each subject
    for subject_id, stats in subject_performance.items():
        if stats['students_appeared'] > 0:
            stats['pass_percentage'] = (stats['students_passed'] / stats['students_appeared']) * 100

    
    # Get all teacher details (faculty details)
    faculty_details = result_analysis_helper.getallteachers_details()
    # Create a lookup dictionary to map faculty_id to full name
    faculty_lookup = {faculty['user_id']: f"{faculty['first_name']} {faculty['last_name']}" for faculty in faculty_details}
    # Iterate over filtered subjects
    for subject_id, subject in filtered_subjects.items():
        # Get the faculty-subject mapping for the given subject_id and ay_id
        subject_mapping = result_analysis_helper.getfaculty_subject_mapping(subject_id, ay_id,course_id,pattern_id,sem_id)
        # Iterate over the subject mapping to extract faculty names and map to subject_id
        for mapping in subject_mapping:
            faculty_id = mapping['faculty_id']
            subject_id = mapping['subject_id']
            # Get the full faculty name from the lookup
            faculty_name = faculty_lookup.get(faculty_id)
            
            if faculty_name:
                # Store faculty name and subject_id in the dictionary
                subject_performance[subject_id]['faculty_name'] = faculty_name
    return subject_performance

#Analyze Exam Performance
def analyze_exam_performance(marks_data):
    performance_summary = {
        'total_students': 0,
        'total_appeared': 0,
        'total_passed': 0,
        'total_failed': 0,
        'total_absent': 0,
        'total_fail_with_atkt': 0,
        'pass_percentage': 0.0,
        'pass_with_atkt_percentage': 0.0
    }

    # Iterate through each student's marks data
    for student in marks_data:
        performance_summary['total_students'] += 1
        
        subjects = student['subjects']
        student_appeared = False
        student_absent=False
        # Check each subject's performance for the student
        for subject_id, subject_data in subjects.items():
            # Check if the student is absent (grade_id == 9)
            if 'grade_id' in subject_data and subject_data['grade_id'] == 9:
                student_absent=True
                continue  # Skip further checks for this subject since the student is absent

            # If the student appeared (has ext_marks or int_marks)
            if 'ext_marks' in subject_data or 'int_marks' in subject_data:
                student_appeared = True

        if student_absent:
            performance_summary['total_absent'] += 1
        # Update total appeared
        if student_appeared:
            performance_summary['total_appeared'] += 1
        # Now, use the student-level status to classify pass/fail/fail with ATKT
        student_status = student.get('status', 'Fail')

        if student_status == 'Pass':
            performance_summary['total_passed'] += 1
        elif student_status == 'Fail':
            performance_summary['total_failed'] += 1
            performance_summary['total_fail_with_atkt'] += 1
        elif student_status == 'Fail with ATKT':
            performance_summary['total_failed'] += 1
            performance_summary['total_fail_with_atkt'] += 1

    # Calculate percentages
    if performance_summary['total_appeared'] > 0:
        performance_summary['pass_percentage'] = (performance_summary['total_passed'] / performance_summary['total_appeared']) * 100
        performance_summary['pass_with_atkt_percentage'] = ((performance_summary['total_passed'] + performance_summary['total_fail_with_atkt']) / performance_summary['total_appeared']) * 100

    return performance_summary

#Extract Top Three Ranker
# Function to get the user details
def get_user_details(user_id, student_data_dict):
    for student in student_data_dict:
        if student['user_id'] == user_id:
            return {
                'first_name': student['first_name'],
                'last_name': student['last_name'],
                'image_main_url': student['image_main_url']
            }
    return None

# Function to get the course name
def get_course_name(course_id, course_dict):
    for course in course_dict:
        if course['id'] == course_id:
            return course['course_name']
    return None

# Function to get the semester name
def get_semester_name(sem_id, semester_dict):
    for semester in semester_dict:
        if semester['id'] == sem_id:
            return semester['semester_name']
    return None

# Function to get the academic year
def get_academic_year(ay_id, academic_year_dict):
    for ayear in academic_year_dict:
        if ayear['id'] == ay_id:
            return ayear['ayear']
    return None

def extract_top_rankers(marks_data,student_data_dict, course_dict, semester_dict, academic_year_dict, top_n=3):
    # Create a list to store user data with their SGPA
    ranked_students = []
    # Iterate over each student's data
    for student in marks_data:
        # Check if 'sgpa' exists and is not 'N/A' or None
        if student.get('sgpa') not in ['N/A', None]:
            user_data = {
                'user_id': student['user_id'],
                'course_id': student['course_id'],
                'sem_id': student['sem_id'],
                'ay_id': student['ay_id'],
                'pattern': student['pattern'],
                'sgpa': float(student['sgpa'])  # Convert SGPA to float for sorting
            }
            ranked_students.append(user_data)

    # Sort the list by SGPA in descending order (top rankers first)
    ranked_students = sorted(ranked_students, key=lambda x: x['sgpa'], reverse=True)

    # Assign rank and extract the top N students (default to top 3)
    top_rankers = []
    for idx, student in enumerate(ranked_students[:top_n], start=1):
        student['rank'] = idx
        top_rankers.append(student)

    ranker_details = []
    
    for ranker in top_rankers:
        user_details = get_user_details(ranker['user_id'], student_data_dict)
        course_name = get_course_name(ranker['course_id'], course_dict)
        semester_name = get_semester_name(ranker['sem_id'], semester_dict)
        academic_year = get_academic_year(ranker['ay_id'], academic_year_dict)
        
        if user_details:
            ranker_details.append({
                'rank': ranker['rank'],
                'sgpa': ranker['sgpa'],
                'full_name':user_details['first_name']+' '+ user_details['last_name'],
                'image_main_url': user_details['image_main_url'],
                'course_name': course_name,
                'semester_name': semester_name,
                'academic_year': academic_year
            })
    
    return ranker_details

    
def faculty_analysis(request):
    context={}
    context=commonhelper.get_login_user_common_context(request.user,context)
    course_and_ay_id_details=[]
    Student_Internal_Marks=[]
    student_data=commonhelper.getallstudent_details()
    for stud_data in student_data:
        course_and_ay_id_details.extend(commonhelper.get_course_id_ay_id_by_userid((stud_data['user_id'],)))
        
    course_details=commonhelper.getallcourse()
    semester_details=commonhelper.getallsemester()
    subject_details=json.dumps(commonhelper.getallsubjects())
    
    acedemic_year=commonhelper.getallacademicyear()
    pattern=commonhelper.getallpatterns()
    grade_data=commonhelper.getallgrade()
    context['course_details']=course_details
    context['semester_details']=semester_details
    context['subject_details']=subject_details
    subject_details = json.loads(subject_details)
    context['acedemic_year']=acedemic_year
    context['pattern']=pattern
    context['student_data']=json.dumps(student_data or {}) #json.dumps for handling null values
    course_and_ay_id_details=json.dumps(course_and_ay_id_details or {})
    context['course_and_ay_id_details']=course_and_ay_id_details
    course_and_ay_id_details=json.loads(course_and_ay_id_details) 
    if request.method=="GET":
    
        return render(request,"faculty/faculty_analysis.html",context)
    
    if request.method=="POST":
        status=False
        try:
            # Parse the JSON string into a Python list
            #filters = json.loads(request.POST.get('filters',''))
            filters={     "course_id": request.POST.get('course-select'),
                          "sem_id": request.POST.get('semester-select'),
                          "ay_id": request.POST.get('ay-select'),
                          "pattern":request.POST.get('pattern-select'),
                          "pattern_id":result_analysis_helper.get_pattern_id(request.POST.get('pattern-select'))
                    }
            assignment_marks=result_analysis_helper.getallAssignmentMarks(**filters)
            mcq_marks=result_analysis_helper.getallMCQMarks(**filters)
            midterm_marks=result_analysis_helper.getallMidTermMarks(**filters)
            endterm_marks=result_analysis_helper.getallEndTermMarks(**filters)
            sub_viva_marks=result_analysis_helper.getallSubjectVivaMarks(**filters)
            opencourse_marks=result_analysis_helper.getallOpenCourseMarks(**filters)
            practical_marks=result_analysis_helper.getallPracticalMarks(**filters)
            miniproject_marks=result_analysis_helper.getallMiniProjectMarks(**filters)
            majorproject_marks=result_analysis_helper.getallMajorProjectMarks(**filters)
            softskills_marks=result_analysis_helper.getallSoftSkillsMarks(**filters)
            sub_ext_marks=result_analysis_helper.getallStudent_Subject_ExternalMarks(**filters)
            ID_OC_SoftSkills=[6,7,10,16,17,20,26,27,30]
            # Combine all lists into one for easier processing
            # Combine only non-empty lists into all_lists
            all_lists = []
            all_lists1 = []

            # Check and add non-empty lists
            for marks_list in [assignment_marks, mcq_marks, midterm_marks, endterm_marks, sub_viva_marks]:
                if marks_list:  # Only add if list is not empty
                    all_lists.append(marks_list)
                    
            final_result=CombineListInDict(all_lists)
            for item in final_result:
                Int_marks=result_analysis_helper.Calculate_Internal_Marks(**item)
                Student_Internal_Marks.append(Int_marks)
          
            for marks_list1 in [sub_ext_marks, Student_Internal_Marks, opencourse_marks, practical_marks, miniproject_marks, majorproject_marks, softskills_marks]:
                if marks_list1:  # Only add if list is not empty
                    all_lists1.append(marks_list1)
            final_Int_Ext_Marks=CombineListInDict(all_lists1)
            for item in final_Int_Ext_Marks:  
                if 'int_marks'in item and 'ext_marks' in item:
                    item["tot_marks"]=item['int_marks']+item['ext_marks']
                else:
                    item["tot_marks"]=item['int_marks']
            Marks=combined_marks(final_Int_Ext_Marks)
            #Check ATKT Subject
            Marks=process_user_marks(Marks,subject_details)
            #Assign Grade To Open Course and Soft Skills
            Marks=assign_grade_id(Marks, ID_OC_SoftSkills)
            
            
            # Filtered dictionary
            filtered_subjects = {}
            for subject in subject_details:
                if(subject['course_id'] == int(filters['course_id']) and 
                    subject['sem_id'] == int(filters['sem_id']) and 
                    subject['subject_pattern'] == filters['pattern']):
                    # Add to the filtered_subjects dictionary
                    filtered_subjects[subject['id']] ={"subject_code":subject['subject_code'],'subject_name':subject['subject_name']} 
                    
            context['filtered_subjects']=filtered_subjects
            
            # Get all user IDs from the Int_Ext_Marks
            user_ids = [user['user_id'] for user in Marks]
            
            # Adding roll_number to Marks dictionary by matching fields
           
            for mark in Marks:
                for course in course_and_ay_id_details:
                    if (
                        mark['user_id'] == course['user_id'] and
                        mark['course_id'] == course['course_id'] and
                        mark['sem_id'] == course['current_semester_id'] and
                        mark['ay_id'] == course['ay_year_id']
                    ):
                        mark['roll_no'] = course['roll_no']
                        break  # Stop searching once a match is found
            # import pdb;pdb.set_trace()
            # Sorting the list of dictionaries by roll_number
            # Marks = sorted(Marks, key=lambda x: x['roll_no'])
            context['Int_Ext_Marks']=Marks
            # Correct context assignment
            context['user_full_names'] = get_user_full_names(student_data,user_ids)
            context['ID_OC_SoftSkills']=ID_OC_SoftSkills
            # Create a dictionary to map grade_id to grade_name
            context['grade_dict'] = {grade['id']: grade['grade_name'] for grade in grade_data}
            
            #Calculating Grade Count
            context['grade_count']=Calculate_Grade_Count(Marks)
            
            #Subject-wise Student Performance Summary
            context['subject_performance']=Subject_wise_Student_Performance(filtered_subjects,filters["ay_id"],filters["course_id"],filters["pattern_id"],filters["sem_id"],Marks)
            #Exam Performance
            context['exam_performance']=analyze_exam_performance(Marks)
            #Top Rankers
            context['top_rankers']=extract_top_rankers(Marks, student_data, course_details, semester_details, acedemic_year, top_n=3)
            #Filter Names
            filters['course_name']=get_course_name(int(filters['course_id']), course_details)
            filters['sem_name']=get_semester_name(int(filters['sem_id']), semester_details)
            filters['year_name']=get_academic_year(int(filters['ay_id']), acedemic_year)
            context['filters']=filters
         
            status=True
        except json.JSONDecodeError as e:
            return JsonResponse({'status': 'error', 'message': "Something went wrong. Please try again or contact support."})
        if status:
          return render(request,"faculty/faculty_analysis.html",context)
        else:
            return JsonResponse({'status': 'error', 'message': "Something ffff went wrong. Please try again or contact support."})
            
def faculty_predictions(request):
    context={}
    context=commonhelper.get_login_user_common_context(request.user,context)
    if request.method=="GET":

        return render(request,"faculty/faculty_predictions.html",context)
