import d2lvalence.auth as d2lauth
import requests

import config

class LampAPI:
    def __init__(self):
        self.host = config.host
        self.app_context_ = d2lauth.fashion_app_context(
            app_id = config.app_id,
            app_key = config.app_key
        )
        self.auth_url_ = self.app_context_.create_url_for_authentication(
            self.host, 
            config.target
        )
        print(self.auth_url_)
        
    def auth(self):
        redirect_url = self.auth_url_
        route = '/d2l/api/versions/'

        user_session = self.app_context_.create_user_context(
            result_uri = redirect_url, 
            host = self.host, 
            encrypt_requests=True
        )
        url = user_session.create_authenticated_url(route)
        r = requests.get(url)
        print(r.status_code)

test = LampAPI()
<<<<<<< HEAD:RestAPI/src/LampAPI/auth.py
test.auth()
=======
#test.auth()
>>>>>>> master:RestAPI/src/LampAPI/lamp.py

