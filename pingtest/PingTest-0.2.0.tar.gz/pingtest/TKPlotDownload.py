        #---------Imports
from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as Tk
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from sqlalchemy import create_engine
import pandas
import time
from subprocess import Popen, PIPE
import shlex
import re
import mysql.connector
import datetime
import threading

#---------End of imports

def TKPlotDownload():

    fig = plt.Figure()

    def __init__(self):
        threading.Thread.__init__(self)
 #       self.ind = ind
 #       self.lock = lock

    def myanimate(i):
        sqlEngine       = create_engine('mysql+pymysql://colin:colin@127.0.0.1/colin', pool_recycle=3600)
        dbConnection    = sqlEngine.connect()
        #line             = pandas.read_sql("select uploadspeed from colin.downloadtest where testdatetime > curdate");
        line             = pandas.read_sql("select downloadspeed from colin.downloadtest where testdatetime > curdate()-1 ", dbConnection);
        pandas.set_option('display.expand_frame_repr', False)
        line, ax.plot(line)
        print(line)
        #plt.show()
        #line.set_ydata(np.sin(x+i/10.0))  # update the data

        return line,

    root = Tk.Tk()
    root.title("ISP Download Speed")

    #label = Tk.Label(root,text="SHM Simulation").grid(column=0, row=0)

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().grid(column=0,row=1)


    ax = fig.add_subplot(111)
    ax.set_title('ISP Download Speed Mbits per sec')
    ax.legend()
    ax.set_xlabel('Recent Readings Last Day')
    ax.set_ylabel('Mbits per second')
    line, = ax.plot([],[])


    #ani = animation.FuncAnimation(fig, myanimate, np.arange(1, 200), interval=250, blit=False)
    ani = animation.FuncAnimation(fig, myanimate, frames=1, repeat=True, interval=5000 , blit=False)

    Tk.mainloop()

def main():

    TKPlotDownload()

if __name__ == '__main__':
    main()
