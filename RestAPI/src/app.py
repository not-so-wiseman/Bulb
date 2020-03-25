import requests
import json
from flask import Flask, Response, redirect, request


from .LampAPI.lamp import Lamp
from .LampAPI.authenticate import Authenticate


app = Flask(__name__)


def validate_api(endpoint_func):
    def wrapper(*args, **kwargs):
        try:
            token = request.args.get("token")
        except KeyError:
            return json.dumps({"message": "Token is missing"}), 403

        api = Lamp(token)
        return endpoint_func(api, *args, **kwargs)
    return wrapper


# Authentification routes

@app.route('/', methods=['GET', 'PUT', 'POST'])
def home():
    return "Welcome to Bulb!"

@app.route('/auth', methods=['GET'])
def authenticate():
    auth = Authenticate()
    return json.dumps(auth.get_auth_url())


# Course information routes

@app.route('/api/courses', methods=['GET'])
@validate_api
def courses(api):
    try:
        return str(api.courses())
    except Exception as e:
        return str("[{}] {}".format(404,e))