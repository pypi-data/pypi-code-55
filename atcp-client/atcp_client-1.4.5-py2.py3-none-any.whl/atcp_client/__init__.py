import threading as th
import socket as sk
import arsa
import abc


class ConnectionObjectError(BaseException):
    def __init__(self, *args):
        self.args = args


class Connection(object):
    class __Supports(object):
        @staticmethod
        def split(content, target):
            res = []
            content_len = len(content)
            target_len = len(target)
            from_index = 0
            for i in range(content_len - target_len + 1):
                if content[i: i + target_len] == target:
                    res.append(content[from_index: i])
                    from_index = i + target_len
            if from_index != content_len:
                res.append(content[from_index:])

            return res

        @staticmethod
        def recv(socket: sk.socket) -> bytes:
            _content = b''
            while True:
                _content += socket.recv(10240)
                if _content.endswith(b'\\\\\\'):
                    return _content[:-3]

        @staticmethod
        def send(socket: sk.socket, msg: bytes):
            socket.send(msg + b'\\\\\\')

    @abc.abstractclassmethod
    class ActionCallback(object):
        def on_create(self):
            pass

        def on_start(self):
            pass

        def on_started(self):
            pass

        @abc.abstractmethod
        def on_created(self):
            pass

        def on_send(self, mid: int):
            pass

        @abc.abstractmethod
        def on_sent(self, mid: int):
            pass

        @abc.abstractmethod
        def on_recved(self, mid: int, msg: str):
            pass

        def on_kill(self):
            pass

        def on_killed(self):
            pass

        def on_close(self):
            pass

        @abc.abstractmethod
        def on_closed(self):
            pass

    @staticmethod
    class __MessageQueue(object):
        def __init__(self):
            self.__max_mid = -1
            self.__message_queue = []

        def __len__(self) -> int:
            return self.__message_queue.__len__()

        def current(self) -> list:
            return self.__message_queue[0][:]

        def next(self) -> list:
            self.__message_queue.remove(self.current())
            return self.current()

        def add(self, msg: str) -> int:
            self.__max_mid += 1
            self.__message_queue.append([self.__max_mid, msg])
            return self.__max_mid

    def __init__(self, server_ips: (str, str, str), server_ports: (int, int, int), key_length: int = 2048):
        """
        :param server_ips
        :type = str
        The IP of the server.

        :param server_ports
        :type = list
        The ports of the server, which should be format as [main, ipidIA, backup].

        :param key_length
        :type = int
        The binary length of the rsa keys using in the connection. It's 2048 in default.
        """
        self.__server_ips: (str, str, str) = server_ips
        self.__server_ports: (int, int, int) = server_ports
        self.__key_length: int = key_length
        self.__socket: sk.socket = sk.socket()
        self.__message_queue: Connection.__MessageQueue = Connection.__MessageQueue()
        self.__is_alive, self.__is_closed = False
        self.__action_callback: Connection.ActionCallback = Connection.ActionCallback()
        self.__specific_action_callback: dict = {}
        self.__rsa_on = True
        self.__public_key, self.__private_key = arsa.new_keys(self.__key_length)
        self.__remote_public_key = None
        self.__ipid = ''

    def __del__(self):
        self.__is_closed = True
        self.__action_callback.on_closed()

    def set_action_callback(self, action_callback: ActionCallback):
        self.__action_callback = action_callback

    def set_specific_action_callback(self, mid: int, action_callback: ActionCallback):
        self.__specific_action_callback[mid] = action_callback

    def set_rsa_on(self, rsa_on: bool):
        self.__rsa_on = rsa_on

    def __recv_listener(self):
        while not self.__is_closed:
            while self.__is_alive:
                msg = self.__recv()

                mid = self.__message_queue.current()[0]
                if mid == -1:
                    self.__socket.close()
                    self.__is_alive = False
                else:
                    if mid in self.__specific_action_callback.keys():
                        self.__specific_action_callback[mid].on_recved(mid, msg)
                    else:
                        self.__action_callback.on_recved(mid, msg)
                    msg = self.__message_queue.next()
                    self.__send(msg[0], msg[1])

    def __determine_parameters(self):
        pubkey = self.__public_key.get_export()
        Connection.__Supports.send(self.__socket, self.__ipid.encode('utf8') + b'@' + pubkey[0] + b'@' + str(pubkey[1]).encode('utf8'))
        msg = Connection.__Supports.recv(self.__socket)
        Connection.__Supports.split(msg, b'@')

    def start(self):
        """
        Use this method to make the Connection object come to life.
        """
        self.__action_callback.on_create()
        ipid_socket = sk.socket()
        try:
            ipid_socket.connect((self.__server_ips[1], self.__server_ports[1]))
        except ConnectionRefusedError:
            raise ConnectionObjectError('cannot get ipid because the connection was refused')
        self.__is_alive = True
        self.__ipid = Connection.__Supports.recv(ipid_socket)
        ipid_socket.close()

        self.__action_callback.on_start()

        try:
            self.__socket.connect((self.__server_ips[0], self.__server_ports[0]))
        except ConnectionRefusedError:
            raise ConnectionObjectError('cannot establish the connection because the connection was refused')

        self.__determine_parameters()

        self.__is_alive = True
        self.__action_callback.on_started()

        th.Thread(target=self.__recv_listener).start()
        self.__action_callback.on_created()

    def __send(self, mid: int, msg: str):
        self.__action_callback.on_send(mid)

        msg = arsa.encrypt(msg, self.__remote_public_key)
        Connection.__Supports.send(self.__socket, msg)

        self.__action_callback.on_sent(mid)

    def __recv(self):
        msg = Connection.__Supports.recv(self.__socket)
        return arsa.decrypt(msg, self.__private_key)

    def send(self, msg: str) -> int:
        """
        Use this method to send a message to S.
        The message won't be sent immediately unless the message queue is empty.
        Generally, the message will be sent after the last message has gotten its return.

        :param msg
        :type = str
        The message to be sent.
        """
        if msg == 'close':
            raise ConnectionObjectError('permission denied')

        if not self.__is_alive:
            raise ConnectionObjectError('cannot send through a closed connection')

        mid = self.__message_queue.add(msg)
        if self.__message_queue.__len__() == 0:
            self.__send(mid, msg)
        return mid

    def kill(self):
        """
        Use this method to kill the Connection object
        """
        if not self.__is_alive:
            raise ConnectionObjectError('cannot kill a dead object')
        self.__action_callback.on_kill()

        msg = 'close'
        mid = self.__message_queue.add(msg)
        if self.__message_queue.__len__() == 0:
            self.__send(mid, msg)

        self.__action_callback.on_killed()

    def close(self):
        """
        Use this method to close the Connection object.
        """
        if self.__is_alive or self.__is_closed:
            raise ConnectionObjectError('cannot close a connection which has already been closed')

        self.__action_callback.on_close()

        del self
