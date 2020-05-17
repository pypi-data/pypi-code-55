import requests
from bs4 import BeautifulSoup

def get():
    # Requests data from page
    response = requests.get("https://api.ipify.org/?format=text")
    ip = response.text

    return ip