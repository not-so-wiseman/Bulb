import json

class GradeObject:
    EVALUATIONS = ["Assignment", "Midterm", "Quiz", "Project", "Report",\
        "Lab", "Test", "Exam"]

    def _assign_type(self):
        NOT_FOUND = -1
        eval_type = "Other" # Default Category
        for category in self.EVALUATIONS:
            if self.name.find(category) != NOT_FOUND:
                eval_type = category
        return eval_type

    def __init__(self, json_block):
        self.name = json_block["GradeObjectName"]
        points = json_block["DisplayedGrade"].split("/")
        self.points = float(points[0])
        self.weight = float(points[1])
        self.type = self._assign_type()

    def json(self):
        data = {
            "Name": self.name,
            "Points": self.points,
            "Weight": self.weight, 
            "Type": self.type
        }
        return data

    def __repr__(self):
        return "<Grade Object>"


class CourseGrades:
    def _filter_grade_items(self, grade_data):
        items = []
        for grade_obj in grade_data:
            if grade_obj["GradeObjectTypeName"] == "Numeric":
                items.append(GradeObject(grade_obj))
        return items

    def _categorize(self, grades_list):
        sorted_grades = {}
        for item in grades_list:
            sorted_grades[item.type] = item.json()
        return sorted_grades

    def _total_fraction(self):
        num = 0
        denom = 0
        for item in self.items:
            num += item.points
            denom += item.weight
        return num, denom

    def __init__(self, json_data):
        self.items = self._filter_grade_items(json_data)
        self.categorized_items = self._categorize(self.items)
        self._numerator, self._demominator = self._total_fraction() 
    
    def average(self):
        return (self._numerator/self._demominator)*100

    def _achievable_percentage(self, goal):
        remaining_percentage = (100 - self._demominator)/100
        to_achieve = (goal - self._numerator)/remaining_percentage
        return to_achieve

    def achieve(self, goal):
        goal = int(goal)
        percent = self._achievable_percentage(goal)
        json_response = {"gradeToAchieve": int(percent), "Achievable": None}
        if (percent < 100):
            json_response["Achievable"] = "Yes"
        else:
            json_response["Achievable"] = "No"
        return json_response
            
            
        
        
        



