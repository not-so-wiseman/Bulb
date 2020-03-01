import d2lvalence.auth as d2lauth
import requests

APP_CREDS = { 
    'host': 'muntest.brightspace.com',
    'target': 'blub.tech',
    'app_id': 'rumLdUKs14G5okboyjFkmQ', 
    'app_key': 'UL_WoG-mxZNO_vgS0ooGQg' 
}

class LampAPI:
    def __init__(self, credentials):
        self.host = credentials['host']
        self.app_context_ = d2lauth.fashion_app_context(
            app_id = credentials['app_id'],
            app_key = credentials['app_key']
        )
        self.auth_url_ = self.app_context_.create_url_for_authentication(
            self.host, 
            credentials['target']
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

test = LampAPI(APP_CREDS)
#test.auth()

