######################################################################
### Bell View
### Copyright (c) 2020 Jonathan Wilson
### Please refer to help/licence.txt for further information
### File: bvwidget.py
### Description: Customised widgets for Bell View GUI
### Last Modified: 24 May 2020
######################################################################

### load Tk modules

from .bvtk import *


######################################################################
### Banner - Title, author and date
######################################################################

class Banner(Frame):
    def __init__(self,parent,title,items):
        Frame.__init__(self,parent)
        Label(self,text=title,font=('Helvetica-Bold',16)).pack(side=TOP)
        for x in items:
            Label(self,text=x).pack(side=TOP)


######################################################################
### EntryView - view only entry
######################################################################

class EntryView(Label):

    def __init__(self,parent,wraplength,value):
        Label.__init__(self,parent,wraplength=wraplength)
        self.var=StringVar()
        self.config(textvariable=self.var)
        self.set(value)

    def get(self):
        return self.var.get()

    def set(self,value):
        self.var.set(value)




######################################################################
### EntryEdit - editable entry
######################################################################

class EntryEdit(Entry):

    def __init__(self,parent,width,value):
        Entry.__init__(self,parent,width=width)
        self.set(value)

    def set(self,value):
        self.delete(0,END)
        self.insert(0,value)


######################################################################
### CheckBox - single checkbox
######################################################################

class CheckBox(Checkbutton):

    ### __init__ - initialise class

    def __init__(self,parent,text,value):
        Checkbutton.__init__(self,parent,text=text)
        self.var=StringVar()
        self.config(variable=self.var,onvalue='on',offvalue='off')
        self.set(value)

    ### get - get value

    def get(self):
        return self.var.get()

    ### set - set value

    def set(self,value):
        self.var.set(value)


######################################################################
### CheckBoxSet - set of checkboxes
######################################################################

class CheckBoxSet(Frame):

    ### __init__ - initialise class instance

    def __init__(self,parent,items):
        Frame.__init__(self,parent)
        self.vars={}
        self.boxes={}
        for k,t in items:
            self.vars[k]=StringVar()
            self.boxes[k]=Checkbutton(self,text=t)
            self.boxes[k].config(variable=self.vars[k],onvalue='on',offvalue='off')
            self.vars[k].set('off')
            self.boxes[k].pack(side=TOP,anchor=NW)

    ### get - get value of a checkbox

    def get(self,key):
        return self.vars[key].get()

    ### set - set value of a checkbox

    def set(self,key,value):
        self.vars[key].set(value)


######################################################################
### RadioButtonSet - radio button set
######################################################################

class RadioButtonSet(Frame):

    ### __init__ - initialise class instance

    def __init__(self,parent,value,buttons):

        Frame.__init__(self,parent)
        self.var=StringVar()
        self.set(value)

        for t,x in buttons:
            b=Radiobutton(self,text=t,variable=self.var,value=x)
            b.pack(side=TOP,anchor=NW)

    ### get - get value of currently active button

    def get(self):
        return self.var.get()

    ### set - set radio buttons

    def set(self,value):
        self.var.set(value)




######################################################################
### ButtonBar - frame with buttons
######################################################################

class ButtonBar(Frame):
    def __init__(self,parent,buttons,right=10):
        Frame.__init__(self,parent)
        for i,(text,command) in enumerate(buttons):
            b=Button(self,text=text,command=command)
            if i>=right:
                b.pack(side=RIGHT)
            else:
                b.pack(side=LEFT)


######################################################################
### ColourSquare - updatable colour square
######################################################################

class ColourSquare(Canvas):

    ### init

    def __init__(self,parent,hexcolour,app):
        Canvas.__init__(self,parent,width=30,height=15)
        self.app=app
        self.var=StringVar()
        self.var.set(hexcolour)
        self.config(bg='#'+hexcolour)
        self.bind('<Button-1>',self.action_pick)

    ### action_pick

    def action_pick(self,event):
        newrgb,newhex=askcolor(
            parent=self.app.root
            ,initialcolor='#'+self.get()
            ,title='Select colour')
        self.app.refresh_menus()
        if newrgb is not None:
            self.set(newhex[1:])

    ### get

    def get(self):
        return self.var.get()

    ### set

    def set(self,hexcolour):
        self.var.set(hexcolour)
        self.config(bg='#'+hexcolour)

######################################################################
### Class: ScrollListBox - Listbox with scrolling
######################################################################

class ScrollListBox(Frame):

    ### initialise class

    def __init__(self,parent,width,height,default,options):

        # initialise parent class
        Frame.__init__(self,parent)

        # add scrollbar and listbox
        self.scrollbar=Scrollbar(self,orient=VERTICAL)
        self.listbox=Listbox(
            self
            , height=height
            , width=width
            , yscrollcommand=self.scrollbar.set
            , selectmode=BROWSE)
        self.scrollbar.config(command=self.listbox.yview)
        self.scrollbar.pack(side=RIGHT,fill=Y)
        self.listbox.pack(side=LEFT,fill=BOTH,expand=1)

        # populate the listbox
        for x in options:
            self.listbox.insert(END,x)

        # index of default option (or zero if not found)
        i=0
        if default in options:
            i=options.index(default)

        # select default option
        self.listbox.selection_set(i)
        self.listbox.activate(i)
        self.listbox.see(i)

    ### get - get selection

    def get(self):
        return self.listbox.get(ACTIVE)


######################################################################
### Geometry management functions
######################################################################

def add_to_grid(parent,items,padx=5,pady=5):

    for r,c,t,x in items:

        if t:
            w=Label(parent,text=x)
        else:
            w=x

        w.grid(row=r,column=c,padx=padx,pady=pady,sticky=NW)



