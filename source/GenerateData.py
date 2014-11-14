import requests
import json
KEY = "4ac7a33ec4523c4afee23227a08aa208"
TERM_URL = "https://api.uwaterloo.ca/v2/terms/1149/"
SUBJECTS_URL = "https://api.uwaterloo.ca/v2/codes/subjects.json?key="

#Object that defines a mapping from an instructor to a specific course
class Mapping:
    def __init__(self, instructor, class_number, course, time, location):
        self.instructor = instructor
        self.class_number = class_number
        self.course = course
        self.time = time
        self.location = location

subject_list = list()

instructor_mapping = dict()
instructor_list = list()

def build_url(subject):
    return TERM_URL + subject + "/schedule.json?key=" + KEY

def get_instructor_name(name):
    return name.split(',')[1] + " " + name.split(',')[0]

def get_instructor_courses(name):
    text = ""
    for i in instructor_mapping[name]:
        text+= i.instructor + " " + i.course + " " + i.location + " " + i.time + "\n"
    return text


def map_course(instructor, class_number, course, time, location):
    if instructor in instructor_mapping:
        instructor_mapping[instructor].append(Mapping(instructor, class_number, course, time, location))
    else:
        instructor_mapping[instructor] = [Mapping(instructor, class_number, course, time, location)]
        instructor_list.append(instructor)

def build_subject_list():
    source = requests.get(SUBJECTS_URL + KEY).text
    data = json.loads(source)['data']
    for s in data:
        subject_list.append(s["subject"])

def checkNull(element):
    if element == None:
        return "None"
    else:
        return element

build_subject_list()
for subject in subject_list:
    source = requests.get(build_url(subject))
    source = source.text
    data = json.loads(source)
    for i in range(0, len(data["data"])):
        course = data["data"][i]
        if len(course["classes"]) > 0 and len(course["classes"][0]["instructors"]) > 0:
            start_time = checkNull(course["classes"][0]["date"]["start_time"])
            end_time = checkNull(course["classes"][0]["date"]["end_time"])
            days = checkNull(course["classes"][0]["date"]["weekdays"])

            instructor = course["classes"][0]["instructors"][0]
            class_number = course["class_number"]
            catalog_number = course["catalog_number"]
            subject = course["subject"]

            building = checkNull(course["classes"][0]["location"]["building"])
            room = checkNull(course["classes"][0]["location"]["room"])

            map_course(instructor, class_number, subject + catalog_number, days + " " + start_time + "-" + end_time, building + room)
##
#for i in instructor_mapping:
    #mapping = instructor_mapping[i]
    #print(get_instructor_name(i) + ": "),
    #for m in mapping:
        #print("(" + m.course),
        #print(m.location + " "),
        #print(m.time + ")"),
    #print("")

#for i in instructor_list:
    #print i,
    #for j in instructor_mapping[i]:
        #print "(" + j.course + " " + j.location + " " + j.time + ")",
    p#rint("")