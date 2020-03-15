import d2lvalence.auth as d2lauth
import requests, os

from .config import Config

class Lamp:
    def __init__(self):
        config = Config()
        self.host = config.get_host()
        self._app_context = d2lauth.fashion_app_context(
            app_id = config.get_id(),
            app_key = config.get_key()
        )
        
    def get_auth_url(self):
        """
            **Builds a URL for user authentication**
            Provides a url that the student can login to their D2L
            account from. This url will redirect the student back to the 
            Bulb's login endpoint.

            :return: URL for authenticating a user 
        """
        _auth_url = self._app_context.create_url_for_authentication(
            self.host + '/login', 
            config.target
        )
        return _auth_url

    
    def _auth_user(self):
        user_session = self._app_context.create_user_context(
            result_uri = None, 
            host = self.host, 
            encrypt_requests=True
        )
        return user_session

    def _get(self, route):
        user_session = self._auth_user()
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



