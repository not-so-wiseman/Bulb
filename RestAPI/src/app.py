import requests
import json
from flask import Flask, Response, redirect, request


from .LampAPI.lamp import Lamp
from .LampAPI.authenticate import Authenticate
from .LampAPI.utils.utilities import Utilities


app = Flask(__name__)
api = Lamp()

@app.route('/', methods=['GET', 'PUT', 'POST'])
def home():
    return "Welcome to Bulb!"

@app.route('/auth', methods=['GET'])
def authenticate():
    print('\n ------auth-------- \n')
    auth = Authenticate()
    return json.dumps(auth.get_auth_url())


@app.route('/api/courses', methods=['GET'])
def courses():
    return request.args
   