import requests
import json
from flask import Flask, Response, redirect, request


from .LampAPI.lamp import Lamp

app = Flask(__name__)
api = Lamp()

@app.route('/', methods=['GET'])
def authenticate():
    return "This is Bulb!"

@app.route('/auth', methods=['GET'])
def authenticate():
    redirect_url = api.get_auth_url()
    return redirect(redirect_url, code=302)

@app.route('/login', methods=['GET'])
def login():
    return json.dumps(api.get_auth_url())
   