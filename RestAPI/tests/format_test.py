import json
from datetime import datetime

class Course:
    def __init__(self, json_elem):
        self.start_date = datetime.strptime(
            json_elem["Access"]["StartDate"],
            '%Y-%m-%dT%H:%M:%S.%fZ'
        )
        self.id = json_elem["OrgUnit"]["Id"]
        self.name = json_elem["OrgUnit"]["Name"]
        data = {"Id":self.id, "Name":self.name, "StartDate":str(self.start_date)}
        self.json = json.dumps(data, indent=4)
    
    def __str__(self):
        return self.json

    def __repr__(self):
        return "<D2L Course Offering>"


test_file = open("response.json", "r")
json_data = json.loads(test_file.readlines()[0])
json_data = json_data["Items"]

active_courses = []

for course in json_data:
    details = course["Access"]
    end_date = details["EndDate"]

    if(details["CanAccess"] == True and details["EndDate"] != None):
        end_date = datetime.strptime(end_date, '%Y-%m-%dT%H:%M:%S.%fZ')
        delta = end_date - datetime.now()
        if(delta.total_seconds() > 0):
            active_courses.append(Course(course))


for course in active_courses:
    print(str(course))

