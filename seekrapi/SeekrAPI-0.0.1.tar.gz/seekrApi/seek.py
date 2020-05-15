
from seekrApi.api import API
from seekrApi.endpoint import Endpoint

class seekrApi:
    def __init__(self, name, flask):
        self.__endpoints = []
        self.__set(flask)
        flask.register_blueprint(API(info={"endpoint":self.__endpoints, "name": name}))

    def __set(self, flask):
        attr = [{"url": n.rule, "method": n.methods} for n in flask.url_map.iter_rules()]
        for a in attr:
            self.__endpoints.append(Endpoint(a))
        return

    def getEndpoints(self):
        return self.__endpoints
