import requests
import pickle
from pyquery import PyQuery
from pathlib import Path
from urllib.parse import urlparse, quote, urljoin

class RequestError(Exception):
    pass

class BrowserStorage:
    def __init__(self, browser, path = None):
        self.browser    = browser
        self.path       = None
        self.jar        = None
        self.responses  = None
        self.contents   = None
        if (path != None):
            self.path       = Path(path)
            self.jar        = Path(path, "cookies.pkl")
            self.responses  = Path(path, "responses")
            self.contents   = Path(path, "contents")
            self._mkdir(self.path)
            self._mkdir(self.responses)
            self._mkdir(self.contents)

    def _mkdir(self, path):
        if (not path.exists()):
            path.mkdir()

    def _rmtree(self, path):
        assert path.is_dir()
        for p in reversed(list(path.glob('**/*'))):
            if p.is_file():
               p.unlink()
            elif p.is_dir():
                p.rmdir()

    def load(self):
        if (self.path != None):
            if (self.jar.exists()):
                with self.jar.open("rb") as file:
                    self.browser.session.cookies.update(pickle.load(file))

    def save(self):
        if (self.path != None):
            with self.jar.open("wb") as file:
                pickle.dump(self.browser.session.cookies, file)

    def save_response(self, url, response):
        if (self.path != None):
            maxlen      = 255 - len(str(self.responses))
            truncated   = url[0:maxlen]
            filename    = quote(truncated, safe="")
            responses   = Path(self.responses, filename)
            contents    = Path(self.contents, filename)
            with responses.open("w", encoding="utf-8") as file:
                file.write("URL\n%s\n\n" % url)
                file.write("STATUS CODE\n%d\n\n" % response.status_code)
                file.write("HEADERS\n%s\n\n" % response.headers)
                file.write("COOKIES\n%s\n\n" % self.browser.session.cookies)
            with contents.open("w", encoding="utf-8") as file:
                file.write(response.text)

class Browser:

    def __init__(self, storage = None):
        self.session    = requests.Session()
        self.storage    = BrowserStorage(self, storage)
        self.url        = None
        self.data       = None
        self.response   = None
        self.storage.load()

    def type(self, url):
        if (self.url != None):
            url = urljoin(self.url, url)
        if (callable(url)):
            self.url = url(self.response)
        else:
            self.url = url
        return self

    def enter(self, **args):
        self.request(lambda: self.session.get(self.url, **args))
        return self

    def form(self, form):
        if (callable(form)):
            self.data = form(self.response)
        else:
            self.data = form
        return self

    def fillup(self, form = dict(), selector = "form"):
        html_form   = self.response.html().find(selector)
        action      = html_form.attr("action")
        html_inputs = html_form.children("input")
        input_names = [ e.attr("name") for e in html_inputs.items() ]
        input_values = [ e.attr("value") for e in html_inputs.items() ]
        self.data   = dict(zip(input_names, input_values))
        self.data.update(form)
        self.type(action)
        return self

    def submit(self, **args):
        if (self.data == None):
            self.request(lambda: self.session.post(self.url, **args))
        else:
            self.request(lambda: self.session.post(self.url, data=self.data, **args))
            self.data = None
        return self

    def request(self, fn):
        self.response = fn()
        self.storage.save_response(self.url, self.response)
        if (self.response.status_code != 200):
            raise RequestError("Request failed url=%s status=%d" % (self.url, self.response.status_code))
        self.storage.save()
        self.response.html = lambda: PyQuery(self.response.text)
        return self
