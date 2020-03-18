import requests
import json
from flask import Flask, Response, redirect, request


from .LampAPI.lamp import Lamp
from .LampAPI.authenticate import Authenticate
from .LampAPI.utils.utilities import Utilities


app = Flask(__name__)
api = Lamp()

@app.route('/', methods=['GET'])
def home():
    return "This is Bulb!"

@app.route('/auth', methods=['GET'])
def authenticate():
    return json.dumps(api.get_auth_url())

@app.route('/login', methods=['POST', 'PUT'])
def login():
    data = request.args
    return json.dumps(data)
   