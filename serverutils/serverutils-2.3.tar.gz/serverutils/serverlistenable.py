## A wrapper around the python low-level socket api, made by Tyler Clarke, April 5, 2020.
## Feel free to use and distribute under the terms of any freeware license you care to mention

## When using, just extend the ServerListenable class and define the handle_post and handle_get functions (each with the arguments self, data, and connection).
## And the handle_aux function, if you want to.

## The webserver can be run by creating an object of your extended class, and calling the run function on it.

## Enjoy!

import socket
import json
import mimetypes
from .socketutils import ServerSocket


class TCPServer:
    def __init__(self,host,port,blocking=True):
        self.server=ServerSocket(host,port)
        self.hooks={"handle":[self.hookcontroller,[self.handle]],
                    "init":[self.hookcontroller,[self.listen]],
                    "mainloop":[self.hookcontroller,[self.run]]}
    def initialize(self):
        self.callhook("init")
    def listen(self,lst=5):
        self.server.listen(lst)
    def run(self):
        connection=self.server.wait_until_connection()
        self.callhook("handle",connection,connection.recieveall())
    def hookcontroller(self,hookdict,hook,*args,**kwargs):
        for x in hookdict[hook][1]:
            x(*args,**kwargs)
    def callhook(self,hook,*args,**kwargs):
        self.hooks[hook][0](self.hooks,hook,*args,**kwargs) ## Call the "hook function" with necessary arguments
    def addhookfunct(self,hook,hookfunct):
        self.hooks[hook][1].append(hookfunct)
    def addhook(self,hook,controller=None):
        if controller==None:
            controller=self.hookcontroller
        self.hooks[hook]=[controller,[]]
    def addExtension(self,extension):
        self.addhookfunct("mainloop",extension.run)
    def delhook(self,hook):
        del self.hooks[hook]
    def delhookfunct(self,hook,index):
        del self.hooks[hook][index]
    def _handle(self,connection):
        data=connection.recieveall()
        self.callhook("handle",connection,data)
    def handle(self,connection,data):
        print("HandleHook Called")
    def start(self):
        self.callhook("init")
        while 1:
            self.callhook("mainloop")
