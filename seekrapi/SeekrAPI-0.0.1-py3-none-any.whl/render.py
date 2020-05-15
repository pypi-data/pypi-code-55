
from flask import render_template

class RenderService:
    def __init__(self, info):
        self.__name = info['name']
        return

    def render(self, data):
        return render_template("index.html", data=data, app_name=self.__name)
