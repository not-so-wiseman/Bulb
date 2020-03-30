import d2lvalence.auth as d2lauth
import requests
import os
import json

import PyPDF2

from copy import deepcopy

from .config import Config
from .utils.courses import Courses, Course
from .utils.gradulator import CourseGrades

D2L_LEARNING_ENV = "/d2l/api/le/1.42/"
D2L_LEARNING_PLATFORM = "/d2l/api/lp/1.26/"

class Lamp:
    """
    """


    def __init__(self, token):
        self._token = token.strip('"')

        config = Config()
        self._target = config.get_target()
        self._host = config.get_host()
        
        self._app_context = d2lauth.fashion_app_context(
            app_id = config.get_id(),
            app_key = config.get_key()
        )

    
    def _auth_user(self):
        user_session = self._app_context.create_user_context(
            result_uri = self._token, 
            host = self._host, 
            encrypt_requests=True
        )
        return user_session

    def _get(self, route):
        user_session = self._auth_user()
        url = user_session.create_authenticated_url(route)
        r = requests.get(url)
        #assert r.status_code == 200
        return r

    # Courses General

    def _return_course_info(self):
        route = D2L_LEARNING_PLATFORM + 'enrollments/myenrollments/'
        request = self._get(route)
        return Courses(request.json())

    def courses(self):
        courses_json = []
        for course in self._return_course_info().data:
            courses_json.append(course.json)
        return json.dumps(courses_json)

    def course(self, course_id):
        courses = self._return_course_info()
        return courses.course(course_id)

    def org_units(self):
        return self._return_course_info().org_units()

    # Grades

    def _return_grade_info(self, course_org_unit):
        #https://online.mun.ca/d2l/api/le/1.0/332969/grades/values/myGradeValues/
        route = "{}{}/grades/values/myGradeValues/".format(
            D2L_LEARNING_ENV,
            course_org_unit
        )
        request = self._get(route)
        return CourseGrades(request.json())

    def overall_average(self):
        course_ids = self._return_course_info().org_units()
        course_grades = []
        for course_no in course_ids:
            average = self._return_grade_info(course_no).average()
            course_grades.append(average)
        return sum(course_no)
        
    def average(self, course_no):
        return self._return_grade_info(course_no).average()

    def achieve_goal(self, course_no, goal):
        return self._return_grade_info(course_no).achieve(goal)

    def grades_course(self, course_no):
        return self._return_grade_info(course_no).categorized_items

    def grades_all(self):
        grades_json = []
        courses = self._return_course_info()
        
        for course in courses.data:
            grade_info = self._return_grade_info(course.id)
            course.json["Grades"] = grade_info.categorized_items
            course.json["Average"] = grade_info.average()
            grades_json.append(deepcopy(course.json))
        
        return json.dumps(grades_json)
            
   
    # Calendar
    #https://online.mun.ca/d2l/le/content/335419/topics/files/download/3138479/DirectFileTopicDownload
    def _return_syllabus(self, course_org_unit):
        #https://online.mun.ca/d2l/api/le/1.0/332969/content/toc
        #https://online.mun.ca/d2l/api/le/1.42/335419/content/topics/3138479/file?stream=true
        route = "{}{}/content/toc".format(
            D2L_LEARNING_ENV,
            course_org_unit
        )
        request = self._get(route)
        return request.json()

    def calendar(self, course_org_unit):
        route = "{}{}/content/topics/{}/file".format(
            D2L_LEARNING_ENV,
            course_org_unit,
            3065118
        )
        request = self._get(route)
        pdfReader = PyPDF2.PdfFileReader(request.text)
        pageObj = pdfReader.getPage(0)

        return str(pageObj.extractText())






