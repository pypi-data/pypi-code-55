
import re

class DataService:
    def __init__(self, info):
        self.__data = self.__getDict(info['endpoint'])
        return

    def __removeLast(self, url):
        counter = 0
        while url[-1*(counter+1)] == '/':
            counter += 1
        return url[:-1*counter] if counter else url


    def __getDict(self, info):
        result = {}
        for i in info:
            url = i.getUrl()
            for method in i.getMethod():
                if method not in set(["OPTIONS", "HEAD"]):
                    loneUrl = re.search('^.+?[^<]*', url)
                    param = self.__getParameter(url)
                    tmp = {
                        "url": self.__removeLast(loneUrl.group(0)),
                        "parameter": param
                    }
                    if method in result:
                        result[method].append(tmp)
                    else:
                        result[method] = [tmp]
        return result

    def __getParameter(self, url):
        result = {}
        types = re.findall('<.+?:', url)
        names = re.findall(':.+?>', url)
        for n in range(len(types)):
            result[names[n][1:-1]] = types[n][1:-1]
        return result

    def deliver(self):
        return self.__data
