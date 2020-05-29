#!/usr/bin/python
import requests
from bs4 import BeautifulSoup as bs

def help():
    print("""
    hey now u can use this as a package to:
    - find youtube videos with `pythondl.gettitle("url")`
    - download video from console with `pydownloader`
    - thats it. for now.
    """)

def gettitle(url):
    content = requests.get(url)
    soup = bs(content.content, "html.parser")
    result = {}
    result['title'] = soup.find("span", attrs={"class": "watch-title"}).text.strip()
    return result['title']
