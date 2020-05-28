import yaml
import os
from canvas import Canvas
import time
import requests

def load_config(path='.'):
    _organization_name = "gatech"
    config_file_name = _organization_name + "-conf.yml"
    _config = ""
    with open(os.path.join(path, config_file_name)) as config_file:
        config = yaml.load(config_file)
        _config= config
    return _config


_config = load_config(os.path.expanduser("~/.ta"))
grader = Canvas(base=_config["base"], token=_config["canvas_api"], course=_config["canvas_course"])

#for conference in grader.GetConferences():
#    if len(conference["recordings"]) > 0:
#        for i in conference["recordings"]:
#            print (i["recording_id"])

#student_id = str()
#assignment_id = str(4683)
#score = "75"
#comment = "The student failed to complete the assignment\nAnd they got thse points wrong\n(-10) for poor guessing"
#grader.SubmitGrade(assignment_id, student_id, score, comment, visibility=False)
 

print (grader.GetCourseEnrollments(True))


#for assignment in grader.GetAssignments():
#   print (assignment)

#for student in grader.GetCourseUsers():
#    print (student)

#print (grader.GetAllStudentUserNames())
#x = grader.GetEmails()
#for i in x:
#    print (i)
#print  (grader.GetExternalTools())
