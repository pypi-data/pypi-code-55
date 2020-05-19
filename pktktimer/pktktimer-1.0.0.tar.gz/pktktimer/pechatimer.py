from tkinter import *
import tkinter.font as tkFont
import sys,getopt
class Pktimer():
    def __init__(self,argsv):
        self.curtimeint=21
        self.curslideint = 0
        try:
            opts,args = getopt.getopt(argsv,'d:',['no-zero-slide'])
        except getopt.GetoptError as err:
            print(str(err))
            sys.exit(2)
        for o,a in opts:
            if o=='-d':
                self.curtimeint=int(a)+1
            if o=='--no-zero-slide':
                self.curtimeint=21
                self.curslideint = 1

        self.root = Tk()
        self.curslide = StringVar()
        self.curtime = StringVar()
        self.setslide(self.curslideint)
        self.settime(self.curtimeint)
        self.paused = False

        slidefont = tkFont.Font(family="Courier",size=30)
        timerfont = tkFont.Font(family="Courier",size=50)
        self.slidecounter = Label(self.root,textvariable=self.curslide,font=slidefont)
        self.timer = Label(self.root,textvariable=self.curtime,font=timerfont)
        self.pause = Button(self.root,text="Toggle Pause",command=self.toggle)
        self.nextsb = Button(self.root,text="Force next",command=self.nexts)
        self.prevsb = Button(self.root,text="Force previous",command=self.prevs)
        self.slidecounter.pack()
        self.timer.pack()
        self.pause.pack(expand=YES,fill=BOTH)
        self.nextsb.pack(side=RIGHT,anchor=N)
        self.prevsb.pack(side=LEFT,anchor=N)

        self.update()
        self.root.mainloop()

    def update(self):
        if self.paused==False:
            self.settime()
            if self.curtimeint == 0:
                self.settime(20)
                self.setslide()
            self.root.after(1000,self.update)

    def toggle(self):
        self.paused = not self.paused
        if self.paused==False:
            self.update()
    def setslide(self,s=-1):
        if s==-1:
            self.curslideint+=1
        else:
            self.curslideint = s
        self.curslide.set("Slide: "+str(self.curslideint))
    def settime(self,t=-1):
        if t==-1:
            self.curtimeint -=1
        else:
            self.curtimeint = t
        self.curtime.set(str(self.curtimeint))
    def nexts(self):
        self.setslide(self.curslideint+1)
        self.settime(20)
    def prevs(self):
        self.setslide(self.curslideint-1)
        self.settime(20)

def main():
    pktimer = Pktimer(sys.argv[1:])
