# -*- coding: utf-8 -*-


class ContentTypeEmnu(object):
    APPLICATION_XWWWFORMURLENCODED = "application/x-www-form-urlencoded"
    TEXT_PLAIN = "text/plain" 
    APPLICATION_JSON = "application/json" 
    APPLICATION_XML = "application/xml" 
    TEXT_XML = "text/xml" 
    TEXT_HTML = "text/html" 
    APPLICATION_JAVASCRIPT = "application/javascript" 
    pass

class HeaderEmnu(object):
    CONTENT_TYPE = "Content-Type"
    authorization = "authorization"
    COOKIES="Cookie"
    HOST="Host"
    ACCEPT="Accept"
    REFERER="Referer"
    pass

    
class methodEmnu(object):
    POST = "POST"
    GET = "GET"
    pass