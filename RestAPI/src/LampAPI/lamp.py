import d2lvalence.auth as d2lauth
import requests
import os
import json

from copy import deepcopy

from .config import Config
from .utils.courses import Courses, Course
from .utils.gradulator import CourseGrades
from .utils.calendar import DataScrubber, PDF, Calendar
from .utils.nlp import find_syllabus

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

    def _percentage(self, decimal):
        decimal = round(decimal)
        return "{}%".format(decimal)

    def average(self, course_no):
        average = self._return_grade_info(course_no).average()
        return round(average, 2)

    def overall_average(self):
        course_ids = self._return_course_info().org_units()
        course_grades = []
        for course_no in course_ids:
            average = self._return_grade_info(course_no).average()
            course_grades.append(average)
        return sum(course_grades)

    def remaining(self, course_no):
        remaining = self._return_grade_info(course_no).remaining()
        return round(remaining, 2)

    def overall_remaining(self):
        course_ids = self._return_course_info().org_units()
        course_remaining_percents = []
        for course_no in course_ids:
            percent = self.remaining(course_no)
            course_remaining_percents.append(percent)

        num_courses = len(course_remaining_percents)
        remaining = sum(course_remaining_percents)/num_courses
        return remaining * 100
        
    def achieve_goal(self, course_no, goal):
        return self._return_grade_info(course_no).achieve(goal)

    def grades_course(self, course_no):
        return self._return_grade_info(course_no).categorized_items

    def grades_all(self):
        grades_json = {
            "Overall": {
                "Average": self._percentage(self.overall_average()),
                "Remaining": self._percentage(self.overall_remaining()),
                "Promotion": self._percentage(65)
            },
            "CourseData": None
        }

        courses_json = []
        courses = self._return_course_info()
        
        for course in courses.data:
            grade_info = self._return_grade_info(course.id)
            course.json["Grades"] = grade_info.categorized_items
            course.json["Average"] = self._percentage(grade_info.average()),
            courses_json.append(deepcopy(course.json))
        
        grades_json["CourseData"] = courses_json

        return json.dumps(grades_json)
            

    # Calendar

    def _return_topic_id(self, course_org_unit):
        #ex: https://online.mun.ca/d2l/api/le/1.0/332969/content/toc
        route = "{}{}/content/toc".format(
            D2L_LEARNING_ENV,
            course_org_unit
        )
        request = self._get(route)
        topic_id = find_syllabus(request.json())
        return topic_id

    def course_calendar(self, course_org_unit):
        topic_id = self._return_topic_id(course_org_unit)

        #ex: https://online.mun.ca/d2l/api/le/1.42/335419/content/topics/3138479/file
        route = "{}{}/content/topics/{}/file".format(
            D2L_LEARNING_ENV,
            course_org_unit,
            topic_id
        )
        data_stream = self._get(route).content
        
        calendar = Calendar()
        calendar.add_events_by_stream(data_stream)

        return calendar

    def calendar_full(self):
        org_units = self.org_units()

        full_calendar = Calendar()
        for course_id in org_units:
            full_calendar += self.course_calendar(course_id)

        return full_calendar








