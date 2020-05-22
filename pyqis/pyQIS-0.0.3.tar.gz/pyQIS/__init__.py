"""
    pyQIS - QIS Server Client implementation in Python 3
    Copyright (C) 2020  Sefa Eyeoglu <contact@scrumplex.net> (https://scrumplex.net)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import requests.sessions
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs, unquote

from pyQIS.data import Grade, Semester


class QIS:

    def __init__(self, server_url):
        """
        Initialize an instance of a QIS Client

        This instance can't do any practical requests.

        These are implemented by other classes like HTWKLeipzigQIS for the HTWK Leipzig QIS Server.
        :param str server_url:str
        """

        self.server_url = server_url
        self.session = None
        self.asi = None

    def new_session(self) -> bool:
        self.session = requests.session()
        r = self.session.get(self.server_url, params={"state": "user", "type": 0, "application": "lsf"})
        if not (r.status_code == 200):
            return False  # TODO: Raise Error
        return True

    def login(self, username: str, password: str) -> bool:
        self.new_session()
        r = self.session.post(self.server_url,
                              params={"state": "user", "type": 1},
                              data={"username": username, "password": password},
                              allow_redirects=False)
        if r.status_code == 302:  # Redirection to main menu, meaning login successful
            # Extract asi from landing page
            r = self.session.get(self.server_url, params={"state": "user", "type": 0, "category": "menu.browse",
                                                          "startpage": "portal.vm"})
            doc = BeautifulSoup(r.text, features="lxml")

            for child in doc.body.find(id="navi-main").find_all("a"):
                url = urlparse(child.get("href"))
                qs = parse_qs(url.query)

                if "asi" in qs:
                    self.asi = qs.get("asi")[0]  # All asis are the same. We break at the first occurrence
                    break

            if self.asi is None:  # asi not found in document. Perhaps incompatible server?
                return False  # TODO Raise Error
            return True  # Login successful, api ready
        return False  # Login failed

    def logout(self) -> bool:
        self._assert_session()
        r = self.session.get(self.server_url,
                             params={"state": "user", "type": 4, "category": "auth.logout", "menuid": "logout"},
                             allow_redirects=False)
        if r.status_code == 200:
            self.session = None
            return True
        return False

    def fetch_results(self) -> list:
        raise RuntimeError("This function is not implemented.")

    def _assert_session(self):
        if self.session is None:
            raise RuntimeError("Session is not initialized. Did you successfully login?")


class HTWKLeipzigQIS(QIS):
    def __init__(self, **kwargs):
        QIS.__init__(self, "https://qisserver.htwk-leipzig.de/qisserver/rds")
        self.grade_average_exam_identifier = '9999'

    def _fetch_result_nodes(self):
        nodes = []

        r = self.session.get(self.server_url, params={"state": "notenspiegelStudent", "next": "tree.vm",
                                                      "nextdir": "qispos/notenspiegel/student",
                                                      "asi": self.asi})

        if r.status_code == 200:
            doc = BeautifulSoup(r.text, features="lxml")

            for graduation in doc.find_all("li", {"class": "abschluss"}):
                # in reality there may be only one node? node basically means major
                nodes.append(
                    unquote(
                        graduation.findChildren("a", recursive=False)[0].get("name")))  # by default it is url encoded
            return nodes
        return False  # TODO: Raise Error

    def fetch_results(self) -> list:
        self._assert_session()
        results = []

        nodes = self._fetch_result_nodes()

        for node in nodes:
            r = self.session.get(self.server_url, params={"state": "notenspiegelStudent", "next": "list.vm",
                                                          "nextdir": "qispos/notenspiegel/student",
                                                          "createInfos": "Y", "struct": "auswahlBaum",
                                                          "nodeID": node, "asi": self.asi})
            doc = BeautifulSoup(r.text, features="lxml")
            results_table = doc.body.find("table", attrs={'class': 'recordTable'})
            children = results_table.findChildren("tr")
            # major = _strip_text(children[0].text)  # unused. potentially needed to differentiate multiple majors?

            current_semester = None
            for row in children[1:]:
                tds = row.findChildren("td")
                if len(tds) == 1:
                    value = _strip_text(tds[0].text)

                    if value.startswith("Keine"):  # No data available
                        continue

                    semester_parts = value.split(" ")

                    if len(semester_parts) < 4:
                        continue  # skip invalid semester

                    semester_year = semester_parts[3]

                    if "/" in semester_year:
                        semester_year = semester_year.split("/", 1)[0]

                    try:
                        semester_year = int(semester_year)
                    except TypeError:
                        continue  # skip invalid semester

                    semester_season = "WS" if semester_parts[2] == "Wintersemester" else "SoSe"
                    current_semester = Semester(semester_season, semester_year, self.grade_average_exam_identifier)

                    results.append(current_semester)
                elif len(tds) == 3:
                    exam_id = _strip_text(tds[0].text)

                    description = _strip_text(tds[1].text)

                    grade = _strip_text(tds[2].text)
                    grade = grade.replace(",", ".", 1)  # we want to prepare this for a float conversion

                    try:
                        grade = float(grade)
                    except ValueError:
                        grade = None  # also handles empty grades ("-")

                    current_semester.grades.append(Grade(exam_id, description, grade))

        return results


def _strip_text(text: str) -> str:
    string = text.strip()

    string = string.replace("\r", "")
    string = string.replace("\n", " ")
    string = string.expandtabs(1)
    string = string.strip()
    while "  " in string:
        string = string.replace("  ", " ")

    return string
