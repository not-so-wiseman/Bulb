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
    return "test"

@app.route('/auth', methods=['GET'])
def authenticate():
    print('\n -------------- \n')https://blub.tech/?x_a=VFuR-5Acoid1kFGPy6C5sy&x_b=_pP_aCfTrYdCb-YV2JBAbs&x_c=I0XxlaI6b511fMtEXD1S3jLkB0APT67IfaoDOOKYyyo
    auth = Authenticate()
    return json.dumps(auth.get_auth_url())

@app.route('/login', methods=['POST', 'PUT'])
def login():
    auth = Authenticate()
    data = request.args
    return json.dumps(data)

@app.route('/api/courses', methods=['GET'])
def courses():
    return "www.blub.tech/api/courses"
   