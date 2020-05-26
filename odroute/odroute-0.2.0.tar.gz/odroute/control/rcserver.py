# -*- coding: utf-8 -*-
import socket
import os

from ..exceptions import ODRouteException
from .executor import CommandExecutor

class RCServer:
    """
    exposes a control interface unix datagram socket
    """

    def __init__(self, router, unix_socket):
        self._executor = CommandExecutor(router)
        self._socket = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
        self._socket.setblocking(False)
        self._unix_socket = unix_socket
        os.remove(unix_socket)
        self._socket.bind(unix_socket)

    def __str__(self):
        return '<RCServer unix={}>'.format(self._unix_socket)

    def get_socket(self):
        return self._socket

    def recv_and_handle(self):
        data, address = self._socket.recvfrom(4096)

        try:
            cmd = data.decode().strip()
            result = self._executor.handle_command(cmd)
        except (TypeError, ODRouteException) as e:
            result = 'Error: {}\n'.format(e)

        # how does that signal EAGAIN or EWOULDBLOCK?
        try:
            self._socket.sendto(result.encode(), address)
        except OSError as e:
            print('error sending result: {} - {}'.format(result, e))
