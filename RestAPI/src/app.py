import requests
import json
from flask import Flask, Response, redirect, request


from .LampAPI.lamp import Lamp

app = Flask(__name__)
api = Lamp()

@app.route('/', methods=['GET'])
def home():
    return "This is Bulb!"

@app.route('/auth', methods=['GET'])
def authenticate():
    return json.dumps(api.get_auth_url())

@app.route('/login', methods=['POST'])
def login():
    data = request.args
    return json.dumps(data)
   