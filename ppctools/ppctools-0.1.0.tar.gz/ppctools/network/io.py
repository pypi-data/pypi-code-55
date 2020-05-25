"""High-level socket IO functionality"""

from __future__ import annotations

from typing import TYPE_CHECKING

import socket
from ppctools.terminal import Clr

if TYPE_CHECKING:
    from typing import Any, Optional


class PPCToolsConnection:
    """High-level connection IO functionality"""
    def __init__(self,
                 hostname: str,
                 port: int,
                 colorize: bool = True,
                 echo: bool = True):
        """Create Connection

        Arguments:
            hostname - host name/address
            port - host port
            colorize - mark outgoing messages green
        """
        self._socket = socket.socket()
        self._socket.settimeout(5)
        self._socket.connect((hostname, port))
        self.colorize = colorize
        self.echo = echo
    
    def __del__(self):
        self._socket.close()

    def send(self,
             *args: Any,
             sep: str = ' ',
             end: str = '\n',
             echo: Optional[bool] = None) -> None:
        """Send text message to remote host

        Arguments:
            *args - Anything that may be presented as string
            sep - string separator (default to space)
            end - message's end (default to line break)
            echo - echo message in stdout
        """
        string: str = sep.join([str(i) for i in args]) + end
        self._socket.sendall(string.encode())
        if echo is None:
            echo = self.echo
        if echo:
            if self.colorize:
                print(f'{Clr.GRN}{string}{Clr.RST}', end='')
            else:
                print(string)

    def read(self,
             messagescount: int = 1,
             echo: Optional[bool] = None,
             fixedcount: Optional[int] = 1024,
             ) -> str:
        """Read message from host
        
        Arguments:
            echo - pass bool value to force echo/quiet (by default using self.echo)
            fixedcount - pass int value to force read fixed bytes count
            messagescount - count of messages to read
        """
        message = ''
        for _ in range(messagescount):
            if fixedcount is not None:
                res = self._socket.recv(fixedcount).decode()
                if not res:
                    res = self._socket.recv(fixedcount).decode()
                     
            else:
                result = bytes()
                shatter = self._socket.recv(1024)
                while shatter:
                    result += shatter
                    shatter = self._socket.recv(1024)
                res = result.decode()
            if not res:
                # print('FIXME: WHAT?')
                raise ConnectionError('Connection closed by remote host')
            message += res
        if echo is None:
            echo = self.echo
        if echo:
            print(message, end='')
        return message
