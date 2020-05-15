## Classes for every supported protocol.
## No versioning, protocols should deal with that themselves.

## Every protocol should accept ONLY a ClientSocket object in its init function
## Also, these should all have a run function.

class HTTP11:
    statuspairs={200:'OK',404:'Not Found'}
    def makeStatusRow(stcode):
        '''Return an http status row bytes object'''
        return ("HTTP/1.1 "+str(stcode)+" "+HTTP11.statuspairs[stcode]+"\r\n").encode()
    def makeHeaders(data):
        toreturn="".encode()
        for x,y in data.items():
            toreturn+=(str(x)+": "+str(y)+"\r\n").encode()
        return toreturn
    def parseRequest(data):
        toreturn={}
        copy=data.decode()
        copy=copy.replace("\r","")
        toreturn["rawrequesttext"]=str(copy)
        copy=copy.split("\n\n")
        toreturn["content"]=str(copy[1])
        toreturn["rawheaders"]=str(copy[0])
        toreturn["headers"]={}
        cop=copy[0].split("\n")
        for x in cop[1:]:
            p=x.split(": ")
            toreturn["headers"][p[0]]=p[1]
        top=cop[0].split(" ")
        toreturn["reqtype"]=top[0]
        toreturn["reqlocation"]=top[1]
        return toreturn
    def addContent(content):
        return "\r\n".encode()+content.encode()

class HTTPOutgoing: ## Write counterpart of HTTPIncoming.
    pass
class HTTPIncoming: ## A "reader" for http requests.
    def __init__(self,socket,data):
        self.socket=socket
        self.data=data
##    def checkHTTP(self,data):
##        ## Check if an HTTP request is made properly. Probably return a 500 error if it isn't?
##        ## Returns 0 if it is a functional request, 1 if it is a broken request, and 2 if it isn't even HTTP.
##        if data[
##        return 0
    def getHTTPVersion(self,data):
        return data.split("\n")[0].split(" ")[2][5:]

class HTTPDATA:
        methods=["GET","POST","HEAD","PUT","DELETE","CONNECT","OPTIONS","TRACE","PATCH"]
        statuspairs={"404":"Not Found"}

class Protocol_HTTP:
    def __init__(self):
        self.requests=[]
        self.server=None
    def extend(self,server):
        server.addhookfunct("handle",self.handle)
        for x in HTTPDATA.methods:
            server.addhook("http_handle"+x)
        self.server=server
    def handle(self,connection,data):
        req=HTTPIncoming(connection,data)
        if req.type=="GET":
            self.server.callhook("http_handleget",req)
        elif req.type=="POST":
            self.server.callhook("http_handlehttppost",req)
        elif req.type=="HEAD":
            self.server.callhook("http_handlehead",req)
        elif req.type=="PUT":
            self.server.callhook("http_handleput",req)
        elif req.type=="DELETE":
            self.server.callhook("http_handledelete",req)
        elif req.type=="CONNECT":
            self.server.callhook("http_handleconnect",req)
    def isError(self,statuscode):
        if statuscode[0] in "45":
            return True
        return False
    def getStatusName(self,statuscode):
        return self.statuspairs[statuscode]
    def recieve(self,clientsocket):
        return HTTPIncoming(clientsocket)
