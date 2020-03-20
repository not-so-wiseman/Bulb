import json

class CourseContext:
    def _filter_json(self, json_data):
        json_data = json_data["Items"]
        return json_data

    
    def __init__(self, json_data):
        self.data = self._filter_json(json_data)
        
    