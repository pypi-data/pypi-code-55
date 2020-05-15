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

class HTTPSocket:
    '''The HTTP protocol for ClientSocket transmissions.'''
    def __init__(self,socket):
        self.socket=socket
        self.recvdata=socket.recieve()
    def getHTTPVersion(self,data):
        return data.split("\n")[0].split(" ")[2][5:]
    
class StandardSocket:
    '''The standard protocol in use for a socket with no defined protocol.
Essentially mirrors the socket interface.'''
    def __init__(self,socket):
        self.socket=socket
        self.cache="".encode()
    def sendfile(self,filename,cache=False):
        if cache:
            file=open(filename,"rb")
            self.cache+=file.read()
            file.close()
        else:
            self.socket.s_sendfile(filename)
    def sendtext(self,data,cache=False):
        if cache:
            self.cache+=data.encode()
        else:
            self.socket.s_sendtext(data)
    def sendbytes(self,data,cache=False):
        if cache:
            self.cache+=data
        else:
            self.socket.s_sendbytes(data)
    def emptycache(self,close=True):
        self.socket.s_sendbytes(self.cache)
        if close:
            self.socket.s_close()
    def recieve(self,rcv=1024):
        return self.socket.s_recieve(rcv)
        
