class Protocol_HTTP:
    def __init__(self):
        self.requests=[]
        self.server=None
    def addToServer(self,server): ## The "attachment" function, to add a built protocol to a server.
        server.getHook("handle").addTopFunction(self.handle)
        server.addHook("httpfailure")
        if hasattr(server,"httpfailed"):
            server.getHook("httpfailure").addFunction(server.httpfailed)
        for x in HTTPDATA.methods:
            server.addhook("http_handle"+x)
            if hasattr(server,"handle"+x.lower()): ## A handler function for every purpose! Twenty percent off!
                server.addhookfunct("http_handle"+x,server.__getattribute__("handle"+x.lower()))
            elif hasattr(self,"handle"+x.lower()):
                server.addhookfunct("http_handle"+x,self.__getattribute__("handle"+x.lower()))
        self.server=server
    def handleget(self,connection,request):
        pass
    def handle(self,connection,data):
        try:
            req=HTTPIncoming(connection,data)
            if req.type in HTTPDATA.methods:
                self.server.getHook("http_handle"+req.type).call(connection,req,HTTPOutgoing())
        except:
            return True ## Some simple py-logic. Only go on to any other handle-events in the case that the HTTP request fails.
        return False
    def getStatusName(self,statuscode):
        return self.statuspairs[statuscode]
    def recieve(self,clientsocket):
        return HTTPIncoming(clientsocket)


class HTTPDATA: ## Static constants for HTTP stuff.
        methods=["GET","POST","HEAD","PUT","DELETE","CONNECT","OPTIONS","TRACE","PATCH"]
        statuspairs={"404":"Not Found"}
        templateget='''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>The standard Serverutils HTTP page</title>
</head>
<body>
<h1>Welcome to serverutils! This page is a hard-coded landing page for Serverutils HTTP.</h1>
<p>You are seeing this because you did not override the handle_get function in your server, or you are using an improperly configured server.<br>
In order to get a different page, create an HTML file and use the response.sendFile function.<br>
(Or just write the HTML inline. The beauty of serverutils is that it doesn't give a crap about where the data comes from.)
</p>
</body>
</html>'''


class HTTPIncoming: ## A "reader" for http requests.
    def __init__(self,socket,data):
        self.socket=socket
        self.data=data
        self.type=statusrow[0]
        self.version=statusrow[2][5:]
        self.location=statusrow[1]
        self.headers=data.split("\r\n\r\n")[0].split('\r\n')[1:]
        print(self.headers)
    def getHTTPVersion(self,data):
        return data.split("\n")[0].split(" ")[2][5:]


class HTTPOutgoing: ## Write counterpart of HTTPIncoming.
    def __init__(self,incoming):
        self.headers={}
        self.version=version
        self.status=status
        self.connection=connection
    def send(self):
        self.connection.sendall()
