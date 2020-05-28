"""implement a telnet server.
"""

import socket
import threading
import socketserver

import sys

try:
    from StructuredData.internal import password
except ImportError:
    import password

__version__="5.1" #VERSION#

assert __version__==password.__version__

# pylint: disable=invalid-name

_handler= None
_use_threads= False

class TCPRequestHandler(socketserver.StreamRequestHandler):
    """handle tcp requests."""
    def handle(self):
        # cur_thread = threading.current_thread()
        # print "name", cur_thread.name
        # self.rfile is a file-like object created by the handler;
        # we can now use e.g. readline() instead of raw recv() calls
        sys.stdin= self.rfile
        sys.stdout= self.wfile
        sys.stderr= self.wfile
        while True:
            _handler()
            #self.data = self.rfile.readline().strip()
            #print "{} wrote:".format(self.client_address[0])
            #print self.data
            ## Likewise, self.wfile is a file-like object used to write back
            ## to the client
            #self.wfile.write(self.data.upper())

class ThreadedTCPServer(socketserver.ThreadingMixIn,
                        socketserver.TCPServer):
    """threaded tcp server."""

class ForkTCPServer(socketserver.ForkingMixIn,
                    socketserver.TCPServer):
    """forked tcp server."""

# without this killing the server may leave the
# port unusable for some minutes:
ForkTCPServer.allow_reuse_address = True

def start(host, port, connection_handler, password_hash):
    """start the server."""
    # pylint: disable=global-statement
    global _handler

    def local_handler():
        """local handler function."""
        s= input("password: ")
        #s= getpass.getpass("password: ",sys.stdin)
        if password_hash != password.password_to_hash(s.strip()):
            print("wrong password !")
            sys.exit(0)
        print("\n" * 24)
        connection_handler()

    _handler= local_handler

    if host is None:
        host= socket.gethostname()
    # Create the server, binding to localhost on port 9999
    if _use_threads:
        server = ThreadedTCPServer((host, port), TCPRequestHandler)
    else:
        server = ForkTCPServer((host, port), TCPRequestHandler)

    # Start a thread with the server -- that thread will then start one
    # more thread for each request

    if _use_threads:
        server_thread = threading.Thread(target=server.serve_forever)
        # Exit the server thread when the main thread terminates
        server_thread.daemon = True
        server_thread.start()
        print("Server loop running in thread:", server_thread.name)
    else:
        print("Server loop running")

    server.serve_forever()
    #server.shutdown()
