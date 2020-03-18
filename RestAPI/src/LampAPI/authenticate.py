import d2lvalence.auth as d2lauth
import requests, os

from .config import Config

class Authenticate:
    def __init__(self):
        config = Config()
        self._target = config.get_target()
        self._host = config.get_host()
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
            self._host + '/login', 
            self._target
        )
        return _auth_url

    def parse_token(self, json):
        """
        """
        return json