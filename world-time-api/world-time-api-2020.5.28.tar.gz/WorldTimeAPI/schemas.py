"""
A collection of JSON response schemes from http://Worldtimeapi.org
"""
class JsonScheme:
    """
    Base JSON response scheme class.

    Use children instead.
    """
    def __init__(self,**jsonObj):
        self._data = {}
        for key,item in jsonObj.items():
            if isinstance(self,DateTimeJson):
                if not (key in self.keyList):
                    raise KeyError(f"Only pass json response objects from client. Expected keys: {self.keyList}")
            if isinstance(self,ErrorJson) and key != "error":
                raise KeyError(f"Expected error key")                

            self._data[key] = item

class DateTimeJson(JsonScheme):
    """
    Any valid JSON resonse from acquiring a datetime from timezone endpoint.
    """
    def __init__(self,**jsonObj):
        JsonScheme.__init__(self,**jsonObj)
    @property
    def keyList(self):
        """
        Response object key list.
        """
        return ('abbreviation','client_ip','datetime','day_of_week','day_of_year','dst','dst_from','dst_offset','dst_until','raw_offset','timezone','unixtime','utc_datetime','utc_offset','week_number')      
    @property
    def abbreviation(self):
        """
        The abbreviated timezone name.
        """
        return self._data['abbreviation']
    @property
    def client_ip(self):
        """
        The ip of the client sending the request.
        """
        return self._data['client_ip']
    @property
    def datetime(self):
        return self._data['datetime']
    @property
    def dow(self):
        """
        The day of the week.
        """
        return self._data['day_of_week']
    @property
    def doy(self):
        """
        The day of the year.
        """
        return self._data['day_of_year']
    @property
    def dst(self):
        """
        Boolean to determine if Daylight savings.
        """
        return self._data['dst']
    @property
    def dst_from(self):
        return self._data['dst_from']
    @property
    def dst_offset(self):
        """
        If daylight savings, display the offset.
        """
        return self._data['dst_offset']
    @property
    def dst_until(self):
        return self._data['dst_until']
    @property
    def raw_offset(self):
        return self._data['raw_offset']
    @property
    def timezone(self):
        return self._data['timezone']
    @property
    def unixtime(self):
        return self._data['unixtime']
    @property
    def utc_datetime(self):
        return self._data['utc_datetime']
    @property
    def utc_offset(self):
        return self._data['utc_offset']
    @property
    def week_number(self):
        return self._data['week_number']

class ErrorJson(JsonScheme):
    """
    JSON error response given if failed query but successful connection to server.
    """
    def __init__(self,**jsonObj):
        JsonScheme.__init__(self,**jsonObj)
    @property
    def errMsg(self):
        return self._data['error']

class ListJson:
    """
    List responses from unlisted location queries.
    """
    def __init__(self,*data):
        self._data = data
    @property
    def data(self):
        return self._data
    
