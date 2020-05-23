# -*- coding: utf-8 -*-

import re
import requests

class EdutermClient:
    def __init__(self,apikey):
        if not self.__checkUuid(apikey):
            raise EdutermClientError("API key not valid, not a UUID")

        self.baseurl = "https://api.onderwijsbegrippen.kennisnet.nl/1.0/Query/";
        self.endpoint = ""
        self.apikey = apikey
        self.query = ""


    def setEndpoint(self,endpoint):
        if endpoint:
            self.endpoint = "&endpoint=" + endpoint


    def request(self,query,args={}):
        self.setQuery(query,args)
        self.setData()
        self.setTable()


    def setQuery(self,query,args={}):
        if not query:
            raise EdutermClientError("query not valid, should not be empty")

        arglist = []
        for key in args:
            arglist.append(key + "=" + args[key])

        argstring = ""
        if arglist:
            argstring = "&" + "&".join(arglist)

        self.query = self.baseurl + query + "?api_key=" + self.apikey + self.endpoint + argstring


    def setData(self):
        self.response_data = ""
        self.response_json = {}

        try:
            r = requests.get(self.query)
        except RequestException as e:
            raise EdutermClientConnectionError("connection error")

        self.__checkStatusCode(r.status_code)
        self.response_data = r.text
        self.response_json = r.json()


    def setTable(self):
        self.response_table = []
        for datarow in self.response_json["results"]["bindings"]:
            row = {}
            for columnname in datarow:
                row[columnname] = self.__getTypedValue(datarow[columnname])
            self.response_table.append(row)


    def __checkStatusCode(self,statuscode):
        if statuscode == 200:
            return
        elif statuscode == 401:
            raise EdutermClientConnectionError("not authorized with key %s" % self.apikey)
        elif statuscode == 400:
            raise EdutermClientConnectionError("query invalid")
        else:
            raise EdutermClientConnectionError("unknown status code %s" % statuscode)


    def __getTypedValue(self,celldata):
        if "datatype" not in celldata:
            return celldata["value"]

        if celldata["datatype"] == "http://www.w3.org/2001/XMLSchema#boolean":
            return self.__parseBoolean(celldata["value"])
        elif celldata["datatype"] == "http://www.w3.org/2001/XMLSchema#integer":
            return int(celldata["value"])
        else:
            return celldata["value"]


    def __parseBoolean(self,string):
        if string == "true":
            return True
        return False


    def __checkUuid(self,uuid):
        if re.match(r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$',uuid):
            return True
        return False


class EdutermClientError(Exception):
    """Generic exception for EdutermClient."""
    def __init__(self,msg,original_exception=None):
        if original_exception:
            msg = msg  + (": %s" % original_exception)

        super(EdutermClientError, self).__init__(msg)
        self.original_exception = original_exception


class EdutermClientConnectionError(EdutermClientError):
    """Exceptions that happen in the data retrieval part."""
    def __init__(self,msg,original_exception=None):
        super(EdutermClientError, self).__init__("Error getting data: %s" % msg, original_exception)
        self.original_exception = original_exception
