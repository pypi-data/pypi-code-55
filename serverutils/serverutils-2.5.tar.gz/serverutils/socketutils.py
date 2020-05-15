import socket


## A wrapper around Sockets, for TCP. Any previously defined compatible protocol is accepted.
class ClientSocket:
    '''A wrapper around the underlying socket API, designed for use with a protocol.
All attribute lookups are redirected to the protocol in use, if you really need
to access them just prefix every attribute with s_ (so s_recieve, s_sendtext, s_sendfile, etc)'''
    def __init__(self,sckt,clidata,blocking):  
        self.clidata=clidata
        self.socket=sckt
##        self.protocol=protocol(self)
##    def __getattribute__(self,attr):
##        if attr[0:2]=="s_":
##            return object.__getattribute__(self,attr[2:])
##        else:
##            return self.s_protocol.__getattribute__(attr)
        if not blocking:
            self.socket.setblocking(False)
    def recieve(self,rcv=1024):
        return self.socket.recv(rcv)
    def recievetext(self,rcv=1024):
        return self.recieve(rcv).decode()
    def recieveall(self,chunks=512):
        '''Recieve all available data, and return it.'''
        data="".encode()
        try:
            while 1:
                data+=self.recieve(chunks)
        except: pass
        return data
    def sendfile(self,filename):
        file=open(filename,"rb")
        self.socket.send(file.read())
        file.close()
    def sendtext(self,data):
        self.socket.send(data.encode())
    def sendbytes(self,data):
        self.socket.send(data)
    def close(self):
        self.socket.shutdown(1)
        self.socket.close()

class ServerSocket:
    def __init__(self,host,port,blocking=False):
        self.host=host
        self.port=port
        self.socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socket.bind((host,port))
        self.blocking=False
    def listen(self,amnt=5):
        self.socket.listen(amnt)
    def wait_until_connection(self):
        '''Wait until a connection is recieved, and return a client socket object'''
        self.socket.setblocking(True)
        connection,clientdata=self.socket.accept()
        return ClientSocket(connection,clientdata,self.blocking)
    def get_connection_nonblocking(self):
        '''Get a connection without blocking the program.
Returns None if no connection is found, and returns a client socket otherwise.'''
        self.socket.setblocking(False)
        try:
            connection, clientdata=self.socket.accept()
            return ClientSocket(connection,clientdata,self.blocking)
        except:
            return None
