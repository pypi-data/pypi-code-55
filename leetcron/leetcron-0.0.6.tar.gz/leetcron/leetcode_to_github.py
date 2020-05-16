import requests
import os
from github import Github
import json

PATH, _ = os.path.split(os.path.realpath(__file__))
PATH += '/'

if not os.path.exists(PATH+'config.json'):
    print('Config file not found. Have you run $leetcron setup ?')
    exit()

with open(PATH+"config.json", "r") as jsonFile:
    config = json.load(jsonFile)

if not config:
    print('SOMETHING WENT WRONG')
    exit()

sessionCSRF = config["LEETCODE_COOKIE"]["sessionCSRF"]
sessionID = config["LEETCODE_COOKIE"]["sessionID"]

headers = {
        "Cookie":  'LEETCODE_SESSION=' + sessionID + ';csrftoken=' + sessionCSRF + ';',
        'X-CSRFToken': sessionCSRF,
        'X-Requested-With': 'XMLHttpRequest'
}

res = requests.get("https://leetcode.com/api/submissions/", headers=headers)
if 'submissions_dump' not in res.json():
    print('COULD NOT AUTHENTICATE LEETCODE')
    exit()
submissions = res.json()['submissions_dump']

question_timestamps_path = PATH+"question_timestamps.json"
if os.path.isfile(question_timestamps_path):
    with open(PATH+"question_timestamps.json", "r") as jsonFile:
        question_timestamps = json.load(jsonFile)
else:
    question_timestamps = {}

GITHUB_TOKEN = config["GITHUB"]['token']
REPO_NAME = config["GITHUB"]['username']+"/"+config["GITHUB"]['repo']

g = Github(GITHUB_TOKEN)

repo = g.get_repo(REPO_NAME)
lang_to_extension = {'python3':'.py', 'cpp':'.cpp', 'java':'.java', 'python':'.py',
                    'c':'.c', 'csharp':'.cs', 'javascript':'.js', 'ruby':'.rb', 
                    'swift':'.swift', 'golang':'.go', 'scala':'.scala', 'kotlin':'.kt',
                    'rust':'.rs', 'php':'.php'}

for sub in submissions:
    if sub['status_display'] == 'Accepted' and (sub['title'] not in question_timestamps or sub['timestamp'] > question_timestamps[sub['title']]):
        filename = sub['title']+lang_to_extension[sub['lang']]
        try:
            contents = repo.get_contents(filename)
            repo.update_file(contents.path, sub['title']+' '+str(sub['timestamp']), sub['code'], contents.sha)
        except Exception:
            repo.create_file(filename, sub['title']+' '+str(sub['timestamp']), sub['code'])
        # keep track of timestamp in record
        question_timestamps[sub['title']] = sub['timestamp']
        print(filename, 'uploaded.')

with open(PATH+"question_timestamps.json", "w") as jsonFile:
    json.dump(question_timestamps, jsonFile)





