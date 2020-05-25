import unittest
import socket
import threading
import time
import random
from ppctools.network import PPCToolsConnection

CONNECTINFO = ('localhost', random.randint(1024, 4096))
TOKEN = 'supersecrettoken13987kjc131'
NUMBER1 = 134124

def handle_connection(request):
    request.sendall(b'Welcome! Please check 2 + 2 = 4 ')
    request.recv(1024)
    request.sendall(b'Token: ')
    request.recv(1024)
    request.sendall(b'Ok. Let\'s play!\n')
    time.sleep(0.5)
    request.sendall(b'Give me a number: ')
    number = int(request.recv(1024).decode())
    request.sendall(f'Hmm {number + 10} is it number + 10? '.encode())
    request.recv(1024)
    request.sendall(b'Bye!\n')


def run_server():
    s = socket.socket()
    s.bind(CONNECTINFO)
    s.listen(1)
    r, addr = s.accept()
    del addr
    handle_connection(r)
    r.close()
    s.close()


class TestConnectionClass(unittest.TestCase):
    def setUp(self):
        threading.Thread(target=run_server, daemon=True).start()
        time.sleep(1)  # Wait for server activate


    def test_connection(self):
        print('\n---------- connect dialog begin ----------\n')
        conn = PPCToolsConnection(*CONNECTINFO)
        args = conn.read().split()[3:]
        self.assertEqual(int(args[0]) + int(args[2]), int(args[4]))
        conn.send('Ok')
        self.assertEqual(conn.read(), 'Token: ')
        conn.send(TOKEN)
        conn.read(2)
        conn.send(NUMBER1)
        num = int(conn.read().split()[1])
        self.assertEqual(num, NUMBER1 + 10)
        conn.send('yes')
        conn.read()
        print('\n---------- connect dialog end   ----------')
