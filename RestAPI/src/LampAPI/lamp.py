import d2lvalence.auth as d2lauth
import requests, os

from .config import Config

class Lamp:
    def __init__(self):
        config = Config()
        self._target = config.get_target()
        self._host = config.get_host()
        self._app_context = d2lauth.fashion_app_context(
            app_id = config.get_id(),
            app_key = config.get_key()
        )
    
    def _auth_user(self, token):
        user_session = self._app_context.create_user_context(
            result_uri = token, 
            host = self._host, 
            encrypt_requests=True
        )
        return user_session

    def _get(self, token, route):
        user_session = self._auth_user(token)
        url = user_session.create_authenticated_url(route)
        r = requests.get(url)
        return r

    def enrolled_courses(self):
        route = '/d2l/api/lp/1.0/enrollments/myenrollments/'
        pass

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



