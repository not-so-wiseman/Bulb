import d2lvalence.auth as d2lauth
from flask import Flask, Response, redirect, request
import requests

app = Flask(__name__)

HOST = 'muntest.brightspace.com'

APP_CREDS = { 
    'app_id': 'rumLdUKs14G5okboyjFkmQ', 
    'app_key': 'UL_WoG-mxZNO_vgS0ooGQg' 
}

APP_CONTEXT = d2lauth.fashion_app_context(
    app_id=APP_CREDS['app_id'], 
    app_key=APP_CREDS['app_key']
)

auth_url = APP_CONTEXT.create_url_for_authentication(HOST, 'http://127.0.0.1:5000/login')
print(auth_url)
@app.route('/login', methods=['POST'])
def login():
    response = request.get
    print("->", response)
    """
    redirect_url = 'https://muntest.brightspace.com/d2l/auth/api/token?x_a=rumLdUKs14G5okboyjFkmQ&x_b=QiAsfBfJL_TkyDzWW02xLU3j1X2JECICnUAkFyxrEKM&x_target=http%3A%2F%2Flocalhost%3A8080'
    user_session = APP_CONTEXT.create_user_context(result_uri=redirect_url, host=HOST, encrypt_requests=True)
    
    route = '/d2l/api/versions/'
    url = user_session.create_authenticated_url(route)
    r = requests.get(url)
    """