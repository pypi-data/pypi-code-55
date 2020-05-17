from tkinter import *

class TrafficLights:

    def __init__(self, responselist, hostlist, respomsems, responsetimedate):

        window = Tk()
        window.title("Network STATUS")

        frame = Frame(window)
        #frame = Frame(height=2, bd=1, relief=SUNKEN)
        frame.pack()

        self.color = StringVar()

        self.canvas = Canvas(window, width=550, height=350, bg="white")
        self.canvas.pack()

        self.oval_site1 = self.canvas.create_oval(10, 10, 110, 110, fill="white")
        self.text_site1 = self.canvas.create_text(60, 63,text="DNS")
        self.oval_site2 = self.canvas.create_oval(120, 10, 220, 110, fill="white")
        self.text_site2 = self.canvas.create_text(170, 63,text="Gateway")
        self.oval_site3 = self.canvas.create_oval(230, 10, 330, 110, fill="white")
        self.text_site3 = self.canvas.create_text(280, 63,text="Google IP")
        self.oval_site4 = self.canvas.create_oval(340, 10, 440, 110, fill="white")
        self.text_site4 = self.canvas.create_text(390, 63,text="Google")

        self.text_appendix1 = self.canvas.create_text(20, 140,text="1 - DNS - "+hostlist[0]+" "+respomsems[0]+" - "+responsetimedate[0], anchor='w')
        self.text_appendix2 = self.canvas.create_text(20, 160,text="2 - Gateway - "+hostlist[1]+" "+respomsems[1]+" - "+responsetimedate[1], anchor='w')
        self.text_appendix3 = self.canvas.create_text(20, 180,text="3 - Google IP - "+hostlist[2]+" "+respomsems[2]+" - "+responsetimedate[2], anchor='w')
        self.text_appendix4 = self.canvas.create_text(20, 200,text="4 - Google - "+hostlist[3]+" "+respomsems[3]+" - "+responsetimedate[3], anchor='w')

        #self.color.set('R')

        self.canvas.itemconfig(self.oval_site1, fill=responselist[0])
        self.canvas.itemconfig(self.oval_site2, fill=responselist[1])
        self.canvas.itemconfig(self.oval_site3, fill=responselist[2])
        self.canvas.itemconfig(self.oval_site4, fill=responselist[3])

        #self.

        # w = Label(window, text='Host1               Host2                  Host3                 Host4', fg="black")
        # w.pack()

        window.mainloop()

    def DispLight(responselist, hostlist, respomsems, responsetimedate):
        TrafficLights(responselist, hostlist, respomsems, responsetimedate)

