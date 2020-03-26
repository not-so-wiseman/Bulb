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
    #https://stackoverflow.com/questions/17256602/assertionerror-view-function-mapping-is-overwriting-an-existing-endpoint-functi
    wrapper.__name__ = endpoint_func.__name__
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
        return api.courses()
    except Exception as e:
        return str("[{}] {}".format(500,e))


@app.route('/api/grades-all', methods=['GET'])
@validate_api
def grades_all(api):
    try:
        return api.grades_all()
    except Exception as e:
        return str("[{}] {}".format(500,e))


@app.route('/api/grades/<org_unit>/goal', methods=['GET'])
@validate_api
def course_goal(api, org_unit):
    try:
        goal = request.args.get("goal")
        return json.dumps(api.achieve_goal(course_no=org_unit, goal=goal))
    except Exception as e:
        return str("[{}] {}".format(500,e))