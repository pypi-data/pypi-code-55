
class Endpoint:
    def __init__(self, info):
        self.__url = info['url']
        self.__method = info['method']

    def getUrl(self):
        return self.__url

    def getMethod(self):
        return self.__method
