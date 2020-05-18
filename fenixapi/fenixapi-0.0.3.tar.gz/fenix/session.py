import requests
import datetime
from bs4 import BeautifulSoup
from .exceptions import *
from operator import itemgetter

__all__ = [
    "Session"
    ]

FENIX_SERVICE = "aHR0cHM6Ly9mZW5peC50ZWNuaWNvLnVsaXNib2EucHQvbG9naW4uZG8=" # https://fenix.tecnico.ulisboa.pt/login.do (b64 encoded)
FENIX_SERVICE_URL = f"https://fenix.tecnico.ulisboa.pt/api/cas-client/login/{FENIX_SERVICE}"

class Session:
    def __init__(self):
        self._logged_in = False
        self._session = None

    def __enter__(self):
        return self

    def __exit__(self, *args):
        if self._session is not None:
            self._session.close()

    @property
    def logged_in(self):
        return self._logged_in

    @property
    def session(self):
        return self._session

    def login(self, username, password):
        if self._session is None:
            self._session = requests.Session()
            self._session.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36"

        # Get session cookie and login codes
        req = self._session.get("https://id.tecnico.ulisboa.pt/cas/login")
        jsessionid = self._session.cookies.get_dict()["JSESSIONID"]
        soup = BeautifulSoup(req.content, features="html.parser")
        # Find lt and event id fields
        lt = soup.find("input", {"name": "lt"})["value"]
        eventid = soup.find("input", {"name": "execution"})["value"]

        # Login
        data = {"service": FENIX_SERVICE_URL,
                "username": username,
                "password": password,
                "submit-istid": "Entrar",
                "lt": lt,
                "execution": eventid,
                "_eventId": "submit"}
        
        req = self._session.post(f"https://id.tecnico.ulisboa.pt/cas/login;{jsessionid}?service={FENIX_SERVICE_URL}", data=data, allow_redirects=False)
        if req.status_code != 200:
            raise UndefinedError("Something unexpected has happened. Are you on the latest version of this API?")
        else:
            if "error-message" in req.text:  # Login failed
                raise LoginError("Wrong username or password")
            else:
                self._logged_in = True

                # Get rid of the inquiry presented
                soup = self.get("")
                url = soup.find("a", {"class": "btn btn-default"})["href"][1:]
                self._get(url)

    def get(self, url, prefix="https://fenix.tecnico.ulisboa.pt"):
        """Returns a BeautifulSoup object with the contents of the desired website."""
        r = self._get(url, prefix)
        soup = BeautifulSoup(r.content, features="html.parser")
        return soup

    def _get(self, url, prefix="https://fenix.tecnico.ulisboa.pt"):
        if prefix != "":
            return self._session.get(f"{prefix}/{url}")
        else:
            return self._session.get(url)

    def get_user_image(self, istid, size=100):
        """Retrieves the profile picture of the specified user.
Authentication required."""
        if not self.logged_in:
            raise AuthenticationError("Authentication required")
        
        r = self._get(f"user/photo/ist{istid}?s={size}")
        if r.content[1:4].decode() == "PNG":  # Check magic number
            return r.content
        else:
            raise NotFoundError(f"User ist{istid} not found")

    def get_course(self):
        """Returns the user's course"""
        s = self.get("student")
        return s.h3.contents[0].strip()

    def get_courses(self):
        """Returns every course the user is enrolled in"""
        courses = []
        s = self.get("student")
        tables = s.table
        cs = tables.findAll("h4", {"class": "mtop025"})
        for c in cs:
            courses.append([c.text.strip(), c.a["href"]])
        return courses

    def get_student_name(self, istid):
        """Returns the name of a student, provided he is enrolled in\
one of the user's courses"""
        courses = self.get_courses()
        for course in courses:
            students = self.get(course[1]+"/notas", "")
            entries = students.table.findAll("tr")
            for entry in entries:
                l = entry.findAll("td")
                if l is not None:
                    if len(l) >= 2:
                        if l[0].text == f"ist{istid}":
                            return l[2].text.strip()
        raise NotFoundError(f"Couldn't find user ist{istid}")

    def get_tests(self):
        url = "/student/enroll/evaluations"
        soup = self.get(url)
        table = soup.find("table", {"class": "evallist"})
        tests = []
        tr = table.findAll("tr")
        for cell in tr:
            type_ = cell.find("td")
            if type_ == None:
                continue
            type_ = type_.getText()
            if type_ == "Exame" or type_ == "Teste":
                test = []
                c = 0
                for td in cell.findAll("td"):
                    if c == 4:
                        break
                    if c != 3:
                        test.append(td.getText().strip())
                    else:
                        date_string = td.getText().strip().split(" ")[0]
                        date_list = date_string.split("/")
                        date_list.reverse()
                        number = int(''.join(date_list))
                        test.append(number)
                    c += 1
                tests.append(test)
        tests = sorted(tests, key = itemgetter(3))
        return tests
    

