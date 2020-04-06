import re

def find_syllabus(toc_json):
    table_of_contents = toc_json["Modules"]
    title = r"(admin|outline|general|course|information)"
    outline = r"(syllabus|outline)"

    def match(title, pattern):
        match = re.search(pattern, title.lower)
        if match:
            return True
        else:
            return False
    
    topic_list = None
    for module in table_of_contents:
        if match(module["Title"], title):
            topic_list = module["Topics"]

    assert topic_list != None

    topic_id = None
    for topic in topic_list:
        if match(topic["url"], outline):
            topic_id = topic["TopicId"]

    assert topic_list != None

    return topic_id





