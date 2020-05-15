
from flask import Blueprint
from seekrApi.data import DataService
from seekrApi.render import RenderService
from seekrApi.constant import ASSET

class API(Blueprint):
    def __init__(self, info=None):
        super().__init__("seekrApi_unique_route", __name__, template_folder=ASSET)
        self.__data = DataService(info)
        self.__render = RenderService(info)
        self.__define()

    def __define(self):

        @self.route("/seekrApi", methods=['GET'])
        def getData():
            data = self.__data.deliver()
            return self.__render.render(data)
