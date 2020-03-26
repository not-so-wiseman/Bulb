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
        self.json = {"Id":self.id, "Name":self.name, "StartDate":str(self.start_date)}
        
    def __str__(self):
        return str(self.json)

    def __repr__(self):
        return "<D2L Course Offering>"


class Courses:
    def _filter_enrollments(self, json_data):
        active_courses = []
        json_data = json_data["Items"]
    
        for course in json_data:
            type_ = course["OrgUnit"]["Type"]["Code"]
            id_ = course["OrgUnit"]["Id"]
            details = course["Access"]
            end_date = details["EndDate"]

            if(details["CanAccess"] == True and details["EndDate"] != None and
            id_ != 336252 and id_ != 336459 and type_ == "Course Offering"):
                #end_date = datetime.strptime(end_date, '%Y-%m-%dT%H:%M:%S.%fZ')
                #delta = end_date - datetime.now()
                #delta = end_date - datetime(2019, 12, 25)
                
                #if(delta.total_seconds() > 0):
                active_courses.append(Course(course))
        return active_courses

    
    def __init__(self, json_data):
        try:
            self.data = self._filter_enrollments(json_data)
        except Exception as e:
            raise Exception("Cannot process json, {}".format(e))
    
    def org_units(self):
        ids = []
        for course in self.data:
            ids.append(course.id)
        return ids 

    def course(self, course_id):
        assert (type(course_id) == str),\
            "Invalid course id of type {}".format(type(course_id))
        
        course_lookup = None
        match = False
        for course in self.data:
            if(course.id == course_id):
                course_lookup = course
                match = True
        assert (match == True), "Course id, {} not found.".format(course_id)

        return course_lookup

        
    