## Copyright 2020 Cedarville University

import requests
from requests.auth import HTTPBasicAuth


class Pyaefis:

    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password

    def getaefiscourses(self, courselist, start=0):
        # Get Courses
        # GET https://cedarville.aefis.net/api/courses

        try:
            response = requests.get(
                url="https://cedarville.aefis.net/api/courses",
                params={
                    "start": start,
                },
                auth=HTTPBasicAuth(self.username, self.password),
                headers={
                },
            )
            if response.status_code == 200:
                data = response.json()
                count = data.get('COUNT', 0)
                if count > 0:
                    start += count
                    courselist.extend(data['DATA'])
                    # return  # debugging
                    self.getaefiscourses(courselist, start)
        except requests.exceptions.RequestException:
            print('HTTP Request failed')

    def getaefiscourse(self, courseid):
        try:
            response = requests.get(
                url=f"https://cedarville.aefis.net/api/courses/{courseid}",
                auth=HTTPBasicAuth(self.username, self.password),
                headers={
                },
            )
            if response.status_code == 200:
                data = response.json()
                if data.get('DATA', None):
                    return data['DATA']
        except requests.exceptions.RequestException:
            print('HTTP Request failed')

    def getaefiscourseobjectives(self, courseid, start=0):
        # Get Objectives
        # GET https://cedarville.aefis.net/api/courses/4561/objectives

        try:
            response = requests.get(
                url=f"https://cedarville.aefis.net/api/courses/{courseid}/objectives",
                auth=HTTPBasicAuth(self.username, self.password),
                headers={
                },
            )
            if response.status_code == 200:
                data = response.json()
                count = data.get('COUNT', 0)
                objectives = list()
                if count > 0:
                    return data['DATA']
                else:
                    return None
                #     for objective in data['DATA']:
                #         objectives.append(objective['Description'])
                # return objectives
        except requests.exceptions.RequestException:
            print('HTTP Request failed')
            sys.exit(1)

    def getaefisprograms(self, programlist, start=0):
        # Get Courses
        # GET https://cedarville.aefis.net/api/courses

        try:
            response = requests.get(
                url="https://cedarville.aefis.net/api/programs",
                params={
                    "start": start,
                },
                auth=HTTPBasicAuth(self.username, self.password),
                headers={
                },
            )
            if response.status_code == 200:
                data = response.json()
                count = data.get('COUNT', 0)
                if count > 0:
                    start += count
                    programlist.extend(data['DATA'])
                    # return  # debugging
                    self.getaefisprograms(programlist, start)
        except requests.exceptions.RequestException:
            print('HTTP Request failed')

    def getaefisprogramobjectives(self, programid, start=0):
        # Get Objectives
        # GET https://cedarville.aefis.net/api/courses/4561/objectives

        try:
            response = requests.get(
                url=f"https://cedarville.aefis.net/api/programs/{programid}/objectives",
                auth=HTTPBasicAuth(self.username, self.password),
                headers={
                },
            )
            if response.status_code == 200:
                data = response.json()
                count = data.get('COUNT', 0)
                outcomes = list()
                if count > 0:
                    for outcome in data['DATA']:
                        o = dict()
                        o['name'] = outcome['Outcome'].get('Name')
                        o['description'] = outcome['Outcome'].get('Description')
                        outcomes.append(o)
                return outcomes
        except requests.exceptions.RequestException:
            print('HTTP Request failed')

    def getaefiscoursesections(self, sectionlist, start=0):
        try:
            response = requests.get(
                url="https://cedarville.aefis.net/api/coursesections",
                params={
                    "start": start,
                },
                auth=HTTPBasicAuth(self.username, self.password),
                headers={
                },
            )
            if response.status_code == 200:
                data = response.json()
                count = data.get('COUNT', 0)
                if count > 0:
                    start += count
                    sectionlist.extend(data['DATA'])
                    # return  # debugging
                    self.getaefiscoursesections(sectionlist, start)
                else:
                    return sectionlist
        except requests.exceptions.RequestException:
            print('HTTP Request failed')

    def aefisgetcoursesection(self, coursesectionid):
        try:
            response = requests.get(
                url=f"https://cedarville.aefis.net/api/coursesections/{coursesectionid}",
                auth=HTTPBasicAuth(self.username, self.password),
                headers={
                },
            )
            if response.status_code == 200:
                data = response.json()
                if data.get('DATA', None):
                    return data['DATA']
        except requests.exceptions.RequestException:
            print('HTTP Request failed')
