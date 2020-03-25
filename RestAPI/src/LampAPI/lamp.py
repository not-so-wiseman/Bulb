import d2lvalence.auth as d2lauth
import requests, os

from .config import Config
from .utils.courses import Courses, Course

D2L_LEARNING_ENV = "/d2l/api/le/1.0/"
D2L_LEARNING_PLATFORM = "/d2l/api/lp/1.0/"

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
        route = D2L_LEARNING_ENV + 'enrollments/myenrollments/'
        request = self._get(route)
        print('\n-------------------\n', route, request.status_code)

        return Courses(request.text)

    def courses(self):
        return self._return_course_info().data

    def course(self, course_id):
        courses = self._return_course_info()
        return courses.course(course_id)

    def org_units(self):
        return self._return_course_info().org_units()

    # Grades

    

    """
    def student_grades(self, course):
        #routes = [
        #    'https://online.mun.ca/d2l/api/le/1.0/332969/grades/'.format(course),
        #    'https://online.mun.ca/d2l/api/le/1.0/332969/grades/447653/values/myGradeValue'
        #]
        pass

    def student_syllabus(self, course):
        route = '/d2l/api/le/1.0/{}/content/root/'.format(course)
        pass

    def course_announcements(self, course):
        route = '/d2l/api/le/1.0/{}/news/'.format(course)
        pass
    """


