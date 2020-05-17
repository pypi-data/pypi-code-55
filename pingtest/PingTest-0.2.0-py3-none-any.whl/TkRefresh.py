import tkinter
import time
from pingtest.SpeedTest import SpeedTest
import threading
from subprocess import Popen, PIPE
import shlex
import re
import logging
from pingtest.SetLogging import *
import mysql.connector
import datetime
from pandas import DataFrame
import pandas
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
from sqlalchemy import create_engine
import pymysql
import matplotlib.animation as animation
from pingtest.TKPlotDownload import TKPlotDownload
from pingtest.TKPlotUpload import TKPlotUpload
from pingtest.TkTraceroute import TKTraceroute
from pingtest.TKPingTest import PingTest

UPDATE_RATE = 1000

COUNTER = 1
downspeed = [' ']
uploadspeed = [' ']
testserver = [' ']


class SpeedThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
 #       self.ind = ind
 #       self.lock = lock

    def run(self):
        global downspeed
        global uploadspeed
        global testserver

        speedbit = "speedtest"
        proc = Popen(speedbit, stdout=PIPE, stderr=PIPE)
        out, err = proc.communicate()
        exitcode = proc.returncode
        #print("====================================SSSSSPPPPPPPPPPEEEEEEEEEEDDDDDDDDDDDDD==============================================>")
        #print(str(out))

        if exitcode == 0:
            downspeed = re.findall("Download: \d+.\d+ Mbit/s",str(out))
            print(downspeed)
            uploadspeed = re.findall("Upload: \d+.\d+ Mbit/s",str(out))
            print(uploadspeed)
            testserver = re.findall("Testing.*\d+.\d+.\d+.\d",str(out))
            print(testserver)
            justds = re.findall("\d+.\d",str(downspeed))
            justus = re.findall("\d+.\d",str(uploadspeed))
            print(justds)
            print(justus)
            justts = testserver[0]
        else:
            justds="0"
            justus="0"
            justts="NOT AVAILABLE"
            testserver="NOT AVAILABLE"


        mydb = mysql.connector.connect(
            host="localhost",
            user="colin",
            passwd="colin",
            database="colin")
        mycursor = mydb.cursor()
        now = datetime.datetime.utcnow()
        print("************DATETIME ========"+str(now))

        #sql = "INSERT INTO pingtest(hostname,testdatetime,responsetime,status) VALUES  (%s,STR_TO_DATE(%s,'%Y-%m-%d %H:%i:%S'),%s,%s)"
        sql = "INSERT INTO downloadtest(servername,testdatetime,downloadspeed,uploadspeed) VALUES  (%s,%s,%s,%s)"
        val = (justts,now, justds[0],justus[0])
        mycursor.execute(sql, val)
        mydb.commit()


class TrafficLights(tkinter.Frame):

    responselist = []
    respomsems = []
    responsetimedate = []
    hostlist = []

    def __init__(self, master):

        tkinter.Frame.__init__(self, master)
        #super().__init__(master)
        #self.grid
        self.pack()
        self.create_window()
        self.updater_window()


    def create_window(self):

        def buttonpressed():
            print("BBBBBBBBBBBBUUUUUUUUUUUUUUTTTTTTTTTTTTTTTTTTOOOOOOOOOOONNNNNNNNNNNNNNN")

        #self.color = tkinter.StringVar()

        self.canvas = tkinter.Canvas(root, width=675, height=130, bg="white")
        self.canvas.pack()

        self.oval_site1 = self.canvas.create_oval(10, 10, 110, 110, fill="white")
        self.text_site1 = self.canvas.create_text(60, 63,text="1 DNS")
        self.oval_site2 = self.canvas.create_oval(120, 10, 220, 110, fill="white")
        self.text_site2 = self.canvas.create_text(170, 63,text="2 Gateway")
        self.oval_site3 = self.canvas.create_oval(230, 10, 330, 110, fill="white")
        self.text_site3 = self.canvas.create_text(280, 63,text="3 Google IP")
        self.oval_site4 = self.canvas.create_oval(340, 10, 440, 110, fill="white")
        self.text_site4 = self.canvas.create_text(390, 63,text="4 Google")
        self.oval_site5 = self.canvas.create_oval(450, 10, 550, 110, fill="white")
        self.text_site5 = self.canvas.create_text(500, 63,text="5 Cloudsure IP")
        self.oval_site6 = self.canvas.create_oval(560, 10, 660, 110, fill="white")
        self.text_site6 = self.canvas.create_text(610, 63,text="6 Alpine Insight")

    def update_window(self):

        global COUNTER
        global downspeed
        global uploadspeed
        global testserver

        def ButtonDown():
            print("BBBBBBBBBBBBUUUUUUUUUUUUUUTTTTTTTTTTTTTTTTTTDOWN")
            thread2 = threading.Thread(target= TKPlotDownload())
            thread2.start()

        def ButtonUp():
            print("BBBBBBBBBBBBUUUUUUUUUUUUUUTTTTTTTTTTTTTTTTTTUP")
            thread3 = threading.Thread(target= TKPlotUpload())
            thread3.start()

        def ButtonTrace():
            print("BBBBBBBBBBBBUUUUUUUUUUUUUUTTTTTTTTTTTTTTTTTTTRACE")
            #thread4 = TKTraceroute(hostlist)
            thread4 = threading.Thread(target= TKTraceroute,args=([hostlist]))
            thread4.start()

        #from pingtest.TKPingTest import PingTest

        responselist, hostlist, respomsems, responsetimedate = PingTest()
        #print(responselist)


        # Set colours of ping results
        self.canvas.itemconfig(self.oval_site1, fill=responselist[0])
        self.canvas.itemconfig(self.oval_site2, fill=responselist[1])
        self.canvas.itemconfig(self.oval_site3, fill=responselist[2])
        self.canvas.itemconfig(self.oval_site4, fill=responselist[3])
        self.canvas.itemconfig(self.oval_site5, fill=responselist[4])
        self.canvas.itemconfig(self.oval_site6, fill=responselist[5])

        self.w1 = tkinter.Label(self, text="1 - DNS - "+hostlist[0]+" "+respomsems[0]+" - "+responsetimedate[0], bg=responselist[0], width=60)
        #w1 = tkinter.Label(self, textvariable = w1_textvar, bg=responselist[0])
        self.w2 = tkinter.Label(self, text="2 - Gateway - "+hostlist[1]+" "+respomsems[1]+" - "+responsetimedate[1], bg=responselist[1], width=60)
        self.w3 = tkinter.Label(self, text="3 - Google IP - "+hostlist[2]+" "+respomsems[2]+" - "+responsetimedate[2], bg=responselist[2], width=60)
        self.w4 = tkinter.Label(self, text="4 - Google - "+hostlist[3]+" "+respomsems[3]+" - "+responsetimedate[3], bg=responselist[3], width=60)
        self.w5 = tkinter.Label(self, text="5 - Cloudsure IP - "+hostlist[4]+" "+respomsems[4]+" - "+responsetimedate[4], bg=responselist[4], width=60)
        self.w6 = tkinter.Label(self, text="6 - Alpine - "+hostlist[5]+" "+respomsems[5]+" - "+responsetimedate[5], bg=responselist[5], width=70)
        self.w1.grid(row=10, column=0)
        self.w2.grid(row=20, column=0)
        self.w3.grid(row=30, column=0)
        self.w4.grid(row=40, column=0)
        self.w5.grid(row=50, column=0)
        self.w6.grid(row=60, column=0)


        frame2 = tkinter.Frame(self)
        frame2.grid(row=190, column=0 )
        downbutton = tkinter.Button(frame2,text="DOWNLOAD CHART", fg="blue", command=ButtonDown)
        upbutton = tkinter.Button(frame2,text="UPLOAD CHART", fg="blue", command=ButtonUp)
        tracebutton = tkinter.Button(frame2,text="TRACEROUTE", fg="blue", command=ButtonTrace)
        downbutton.pack(side="left")
        upbutton.pack(side="left")
        tracebutton.pack(side="left")

        if responselist[0] == "red":
            print("LETS DO TRACEROUTE")

        if ( COUNTER == 1):

            print("$$$$$$$$$$$$$$$$$$$$$$$$ FIRST LINE")
            st1 = tkinter.Label(self, text="Test Server - Performing Test",bg="yellow",width=40)
            st2 = tkinter.Label(self, text="Download Speed - Performing Test",bg="yellow",width=40)
            st3 = tkinter.Label(self, text="Upload Speed - Performing Test",bg="yellow",width=40)
            st1.grid(row=100, column=0)
            st2.grid(row=110, column=0)
            st3.grid(row=120, column=0)

        if ( COUNTER % 60 == 0 or COUNTER == 1):
            #print("DOWNLOAD WINDOWS ++++++++++++++++++++++++++++++++"+str(COUNTER))
            #TestingServer, DownLoadSpeed, UpLoadSpeed = SpeedTest()

            thread1 = SpeedThread()
            thread1.start()
            #thread2 = AnimateTinker()
            #thread2.start()
            #print("******************** SPEED TEST **************************************")

        if ( COUNTER % 60 == 0 ):
            #print("WHHHHYYYY HEERRRREEEEE")
            #print(str(downspeed))
            if testserver == "NOT AVAILABLE":
                st1 = tkinter.Label(self, text="Test Server - Not Available",bg="red2",width=40)
                st2 = tkinter.Label(self, text="Downlaod Speed - Not Available",bg="red3",width=40)
                st3 = tkinter.Label(self, text="Upload Speed - Not Available",bg="red4",width=40)
            else:
            #print(TestingServer)
                st1 = tkinter.Label(self, text="Server - "+testserver[0]+")",bg="sea green", width=40)
                st2 = tkinter.Label(self, text="Speed - "+downspeed[0],bg="spring green", width=40)
                st3 = tkinter.Label(self, text="Speed - "+uploadspeed[0],bg="lawn green", width=40)

            st1.grid(row=100, column=0)
            st2.grid(row=110, column=0)
            st3.grid(row=120, column=0)


        COUNTER = COUNTER + 1
        print("Counter ="+str(COUNTER))

    def updater_window(self):
        self.update_window()
        self.after(UPDATE_RATE, self.updater_window)

initialize_logger('/var/log/PingTest')

logging.debug("debug message")
logging.info("info message")
logging.warning("warning message")
logging.error("error message")
logging.critical("critical message")

root = tkinter.Tk()
root.title("Network STATUS")
app = TrafficLights(root)
time.sleep(1)
root.mainloop()
