#---------Imports

import time
from subprocess import Popen, PIPE
import shlex
import re
import mysql.connector
import datetime
import threading
import tkinter as tk
import tkinter.scrolledtext as tkst

#---------End of imports

def TKTraceroute(hostlist):

    def __init__(self):
        threading.Thread.__init__(self)
        #self.ind = ind
        #self.lock = lock

    def test():
        print("TEST")

    tracestring =b''

    for hostcheck in hostlist:
        print(hostcheck)
        tracebit = "traceroute " + hostcheck
        args = shlex.split(tracebit)
        proc = Popen(args, stdout=PIPE, stderr=PIPE)
        out, err = proc.communicate()
        exitcode = proc.returncode
        print(out)
        tracestring += out
        #TraceCheck(hostcheck)

    win = tk.Tk()
    frame1 = tk.Frame(
        master = win,
        bg = '#808000'
        )
    frame1.pack(fill='both', expand='yes')
    editArea = tkst.ScrolledText(
        master = frame1,
        wrap   = tk.WORD,
        width  = 80,
        height = 20
    )
    # Don't use widget.place(), use pack or grid instead, since
    # They behave better on scaling the window -- and you don't
    # have to calculate it manually!
    editArea.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    # Adding some text, to see if scroll is working as we expect it
    editArea.insert(tk.INSERT,tracestring)
    #"""\
    #This is some text
    #I want to insert here
    #""")
    win.mainloop()


def main(hostlist):

    TKTraceroute(hostlist)

if __name__ == '__main__':
    main()




