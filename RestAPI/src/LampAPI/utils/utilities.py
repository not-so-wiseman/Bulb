from .format_json import CourseContext

class Utilities:
    def show_courses(self, json_data):
        cc = CourseContext(json_data)
        return cc.data 