import requests
from bs4 import BeautifulSoup
from .exceptions import *

__all__ = [
    "exists_user",
    "get_name",
    "search_space",
    "Space"
    ]

class Space:
    def __init__(self, location, name, description, link):
        self._location = location
        self._name = name
        self._description = description
        self._link = link
    
    @property
    def location(self):
        return self._location

    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._description

    @property
    def loaded(self):
        return self._loaded

    @property
    def link(self):
        return self._link
        
    
def exists_user(istid):
    """Returns true if the specified user exists."""
    r = requests.get(f"https://fenix.tecnico.ulisboa.pt/user/photo/ist{istid}")
    return r.content[1:4].decode() == "PNG"  # Check magic number

def get_name(istid):
    """Tries to fetch the real name of the user."""
    if not exists_user(istid):
        raise NotFoundError(f"User ist{istid} does not exist")
    r = requests.get(f"https://fenix.tecnico.ulisboa.pt/homepage/ist{istid}")
    soup = BeautifulSoup(r.content, features="html.parser")
    h2 = soup.find("h2", {"class": "site-header"})
    if h2 is None:
        raise NotFoundError(f"User ist{istid} does not have a public webpage")
    name = soup.find("h2", {"class": "site-header"}).a
    if name is None:
        raise NotFoundError(f"User ist{istid} does not have a public webpage")
    return name.text.replace(chr(183), "").strip()
    

def search_space(space):
    r = requests.get("https://fenix.tecnico.ulisboa.pt/conteudos-publicos/pesquisa-de-espacos")
    soup = BeautifulSoup(r.content, features="html.parser")
    viewstate = soup.find("input", {"name": "pt.ist.fenixWebFramework.renderers.components.state.LifeCycleConstants.VIEWSTATE"})["value"]
    search_type = soup.find("label", {"class": "control-label col-sm-2"})["for"]
    search_label = soup.find("input", {"class": "form-control", "type": "text"})["id"]
    data = {"method": "search",
            search_type: "SPACE",
            search_label: space,
            "pt.ist.fenixWebFramework.renderers.components.state.LifeCycleConstants.VIEWSTATE": viewstate}

    r = requests.post("https://fenix.tecnico.ulisboa.pt/publico/findSpaces.do", data=data)
    soup = BeautifulSoup(r.content, features="html.parser")
    table = soup.table
    if table is None:
        return
    table = table.tbody
    entries = table.findAll("tr")
    spaces = []
    for entry in entries:
        defs = entry.findAll("td")
        location = []
        for a in defs[0].findAll("a"):
            location.append(a.text)
        name = a.text
        link = "https://fenix.tecnico.ulisboa.pt" + a["href"]
        location = " > ".join(location)
        classification = defs[1].text.strip()
        
        spaces.append(Space(location, name, classification, link))
    return spaces
    
    
