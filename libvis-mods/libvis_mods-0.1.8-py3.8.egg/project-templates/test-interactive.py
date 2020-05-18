from subprocess import Popen, PIPE

import sys
import os
from queue import Queue, Empty
import subprocess
import threading
import time

class LocalShell(object):
    def __init__(self):
        pass

    def run(self, cmd):
        env = os.environ.copy()
        p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=subprocess.STDOUT, shell=True, env=env)

        def writeall(p):
            while True:
                # print("read data: ")
                data = p.stdout.read(1).decode("utf-8")
                if not data:
                    break
                sys.stdout.write(data)
                sys.stdout.flush()

        writer = threading.Thread(target=writeall, args=(p,))
        writer.start()

        def reader(readq):
            try:
                while True:
                    d = sys.stdin.read(1)
                    if not d:
                        break
                    readq.put(d)
            except EOFError:
                pass

        readq = Queue()
        r = threading.Thread(target=reader, args=(readq,))
        r.daemon=True
        r.start()

        while True:
            if not writer.isAlive():
                break
            try:
                d = readq.get(block=False)
                self._write(p, bytes(d, 'utf-8'))
                time.sleep(0.01)
            except Empty:
                pass

    def _write(self, process, message):
        process.stdin.write(message)
        process.stdin.flush()


cmd = ['cookiecutter', 'source-files']
cmd = ' '.join(cmd)

def main():
    shell = LocalShell()
    try:
        shell.run(cmd)
    except KeyboardInterrupt:
        return

if __name__ == '__main__':
    main()
