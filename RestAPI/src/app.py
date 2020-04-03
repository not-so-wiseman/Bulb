import requests
import json
from flask import Flask, Response, redirect, request, render_template


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
    return render_template('home.html')

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
    return api.grades_all()
    

@app.route('/api/grades/<org_unit>/goal', methods=['GET'])
@validate_api
def course_goal(api, org_unit):
    goal = request.args.get("goal")
    return api.achieve_goal(course_no=org_unit, goal=goal)


@app.route('/api/calendar', methods=['GET'])
@validate_api
def get_topics(api):
    dummyCalendar = {
        "January": [],
        "Febuary": [],
        "March": [
            {"Name":"Assignment 1 Due", "Day":15},
            {"Name":"Midterm", "Day":20}
        ],
        "April": [
            {"Name":"Assignment 2 Due", "Day":27},
            {"Name":"Quiz 1", "Day":3}
        ],
        "May": [],
        "June": [],
        "July":[],
        "August":[],
        "September":[],
        "October": [],
        "November": [],
        "December": []
    }
    return str(dummyCalendar) 
