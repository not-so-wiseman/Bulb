import d2lvalence.auth as d2lauth
from flask import Flask, Response, redirect, request
import requests
import 

app = Flask(__name__)

print(auth_url)
@app.route('/login', methods=['POST'])
def login():
    print("hi")
    """
    redirect_url = 'https://muntest.brightspace.com/d2l/auth/api/token?x_a=rumLdUKs14G5okboyjFkmQ&x_b=QiAsfBfJL_TkyDzWW02xLU3j1X2JECICnUAkFyxrEKM&x_target=http%3A%2F%2Flocalhost%3A8080'
    user_session = APP_CONTEXT.create_user_context(result_uri=redirect_url, host=HOST, encrypt_requests=True)
    
    route = '/d2l/api/versions/'
    url = user_session.create_authenticated_url(route)
    r = requests.get(url)
    """