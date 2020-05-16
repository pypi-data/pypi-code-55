from crontab import CronTab
import sys
import os
import browsercookie
import json
import getpass
import requests
from github import Github

PATH, _ = os.path.split(os.path.realpath(__file__))
PATH += '/'

def getCookie():
    """
    Get cookie of Leetcode session from Chrome or Firefox
    """
    cj = browsercookie.load()
    sessionCSRF = ''
    sessionID = ''

    for cookie in cj:
        if cookie.domain == 'leetcode.com' and cookie.name=='csrftoken':
            sessionCSRF = cookie.value
        if cookie.domain == '.leetcode.com' and cookie.name=='LEETCODE_SESSION':
            sessionID = cookie.value
    
    if not sessionCSRF or not sessionID:
        print('ERROR: Cannot find Leetcode cookies.')
        print('Are you sure you are logged into leetcode in Chrome or Firefox?')
        return
    
    with open(PATH+"config.json", "r") as jsonFile:
        data = json.load(jsonFile)

    data["LEETCODE_COOKIE"]["sessionCSRF"] = sessionCSRF
    data["LEETCODE_COOKIE"]["sessionID"] = sessionID

    with open(PATH+"config.json", "w") as jsonFile:
        json.dump(data, jsonFile)
    
    print('Leetcode cookies saved.')

def setupGithub():
    """
    Set up tool with Github Key and Github repo name
    """
    with open(PATH+"config.json", "r") as jsonFile:
        data = json.load(jsonFile)
    
    username = input("Github Username: ")
    token = input("Github Access Token: ")
    r = requests.get('https://api.github.com', auth=(username, token))

    while r.status_code != 200:
        print('Invalid credentials. Please try again.')
        username = input("Github Username: ")
        token = input("Github Access Token: ")
        r = requests.get('https://api.github.com', auth=(username, token))
    
    repo = input("Repo for Leetcode files: ")
    r = requests.get("https://api.github.com/repos/"+username+"/"+repo, auth=(username, token))
    while r.status_code != 200:
        toCreate = input('This repository does not exist yet. Do you want leetcron to create it for you? (Y/N)')
        
        if toCreate.upper() == 'Y' or toCreate.lower() == 'yes':

            isPrivate = input('Do you want the repository to be private? (Y/N)')
            while isPrivate.lower() not in ['y', 'n', 'yes', 'no']:
                print('Invalid input.')
                isPrivate = input('Do you want the repository to be private? (Y/N)')

            if isPrivate.upper() == 'Y' or isPrivate.lower() == 'yes':
                isPrivate = True
            else:
                isPrivate = False
            
            g = Github(token)
            g.get_user().create_repo(repo, private = isPrivate)
            r = requests.get("https://api.github.com/repos/"+username+"/"+repo, auth=(username, token))
            if r.status_code == 200:
                print('Repo successfully created!')
                break
            else:
                print('Something went wrong. Please try again later or set up the repo manually.')
                break
        else:
            print('Please input the correct repository name.')
            repo = input("Repo for Leetcode files: ")
            r = requests.get("https://api.github.com/repos/"+username+"/"+repo, auth=(username, token))
    
    data["GITHUB"]["username"] = username
    data["GITHUB"]["token"] = token
    data["GITHUB"]["repo"] = repo

    with open(PATH+"config.json", "w") as jsonFile:
        json.dump(data, jsonFile)
    
    print('Github setup successful.')

def setCronJob():
    """
    Create or update the cron job that runs leetcode_to_github.py
    """
    cron = CronTab(user=getpass.getuser())

    found = False
    for j in cron.find_command(sys.executable+" "+PATH+"leetcode_to_github.py"): #need to get full path of file too
        found = True
        job = j

    if not found:
        job = cron.new(command=sys.executable+" "+PATH+"leetcode_to_github.py")

    time = ['*']*5
    time[0] = '0'
    freq = input("How often do you want to run this cron job?\n1. Every hour\n2. Every day\n3. Every week\n4. Every month\n").strip()
    while not freq.isdigit() or int(freq) > 4 or int(freq) < 1:
        print('Please input a number between 1 and 4 (inclusive).')
        freq = input("How often do you want to run this cron job?\n1. Every hour\n2. Every day\n3. Every week\n4. Every month\n").strip()
    
    freq = int(freq)
    if freq == 4:
        f = input('On what day of the month? (Please enter a number between [1, 31] or press enter if no preference)').strip()
        while f and (not f.isdigit() or int(f) > 31 or int(freq) < 1):
            print('Please input a number between 1 and 31 (inclusive).')
            f = input('On what day of the month? (Please enter a number between [1, 31] or press enter if no preference)').strip()
        if not f:
            time[3] = '*/1'
        else:
            time[2] = f
    if freq == 3:
        f = input('On what day of the week? (Please enter a number between [1, 7] or press enter if no preference)').strip()
        while f and (not f.isdigit() or int(f) > 31 or int(freq) < 1):
            print('Please input a number between 1 and 7 (inclusive).')
            f = input('On what day of the week? (Please enter a number between [1, 7] or press enter if no preference)').strip()
        if not f:
            time[4] = '1'
        else:
            time[4] = f
    if freq >= 2:
        f = input('On what hour of the day? (Please enter a number between [0, 23] or press enter if no preference)').strip()
        while f and (not f.isdigit() or int(f) > 23 or int(freq) < 0):
            print('Please input a number between 0 and 23 (inclusive).')
            f = input('On what hour of the day? (Please enter a number between [0, 23] or press enter if no preference)').strip()
        if not f and freq == 2:
            time[4] = '*/1'
        else:
            time[1] = f
    if freq == 1:
        time[1] = '*/1'

    job.setall(' '.join(time))
    # job.minute.every(2)
    cron.write()

    print('Cron job setup successful.')

def setup(option = None):
    #build config file
    if not os.path.exists(PATH+'config.json'):
        if os.path.exists(PATH+'config.example.json'):
            os.rename(PATH+'config.example.json', PATH+'config.json')
        else:
            data = {
                "GITHUB": {
                    "username": "", 
                    "token": "", 
                    "repo": ""
                }, 
                "LEETCODE_COOKIE": {
                    "sessionID": "", 
                    "sessionCSRF": ""
                }
            }
            with open(PATH+"config.json", "w") as jsonFile:
                json.dump(data, jsonFile)
    
    options = {
        "-g": setupGithub,
        "-c": getCookie,
        "-j": setCronJob
    }

    if not option:
        setupGithub()
        getCookie()
        setCronJob()
        print()
        print('You are all set!')
    else:
        options[option]()

def run():
    f = PATH+'leetcode_to_github.py'
    code = compile(open(f).read(), f, 'exec')
    exec(code)