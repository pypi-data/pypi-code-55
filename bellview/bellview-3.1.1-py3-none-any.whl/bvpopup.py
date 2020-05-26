######################################################################
### Bell View
### Copyright (c) 2020 Jonathan Wilson
### Please refer to help/licence.txt for further information
### File: bvpopup.py
### Description: Popups for GUI
### Last Modified: 24 May 2020
######################################################################

### import modules

import os
from crengine import ringing
from crengine.rowfmt import linethickness, hexcolour
from .bvtk import *
from .bvwidget import *

######################################################################
### Class: PopupWindow
######################################################################

class PopupWindow():

    ### init: create a window with a blank form, close and apply buttons

    def __init__(self,parent,name,cancel=False):

        # save to class
        self.parent=parent
        self.name=name

        # capture shell from parent
        self.eng=parent.eng

        # window
        self.root=Toplevel(parent.root)
        self.root.resizable(0,0)
        self.root.title(name)

        # main frame
        frame_main=Frame(self.root)
        frame_main.pack()

        # content
        self.frame_form=Frame(frame_main)
        self.frame_form.pack(side=TOP,anchor=NW,padx=20,pady=20)

        # buttons
        buttons=[]
        if cancel:
            buttons.append(('Cancel',self.action_cancel))
        buttons.append(('OK',self.action_ok))
        frame_button=ButtonBar(frame_main,buttons)
        frame_button.pack(side=TOP,anchor=NE,padx=20,pady=20)

    ### action_ok - action if OK is pressed

    def action_ok(self):
        self.root.destroy()

    ### action_cancel - action if Cancel is pressed

    def action_cancel(self):
        self.root.destroy()

    ### isopen: verify that window is open

    def isopen(self):
        return self.root.winfo_exists()

    ### lift: force window to top

    def lift(self):
        self.root.lift()


######################################################################
### Class: MessageWindow
######################################################################

class AboutWindow(PopupWindow):

    ### init: create popup with text box

    def __init__(self,parent):
        PopupWindow.__init__(self,parent,'About %s' %parent.info['name'])
        non_warranty=self.parent.non_warranty.replace('\n',' ')
        website='For updates please visit %s' %self.parent.info['url']
        self.parent.banner_info(self.frame_form,verbose=True).pack(side=TOP,pady=2)
        Label(self.frame_form,wraplength=400,text=non_warranty).pack(side=TOP,pady=5)
        Label(self.frame_form,text=website).pack(side=TOP,pady=5)


######################################################################
### Class: MessageWindow
######################################################################

class MessageWindow(PopupWindow):

    ### init: create popup with text box

    def __init__(self,parent,title,text,width=80,height=25):
        PopupWindow.__init__(self,parent,'Message')
        self.vbar=Scrollbar(self.frame_form)
        self.txt=Text(
            self.frame_form
            , width=width
            , height=height
            , font=('Courier',14)
            )
        self.vbar.pack(side=RIGHT,fill=Y)
        self.txt.pack(side=LEFT,fill=Y)
        self.vbar.config(command=self.txt.yview)
        self.txt.config(yscrollcommand=self.vbar.set)
        self.root.title(title)
        self.txt.insert(END,text)
        self.txt.configure(state='disabled')
        self.txt.bind("<1>", lambda event: self.txt.focus_set())


######################################################################
### Class: MethodSelectWindow
######################################################################

class MethodSelectWindow(PopupWindow):

    ### init: create config window with method selector

    def __init__(self,parent):
        PopupWindow.__init__(self,parent,'Select Method',cancel=True)
        names=self.eng.crelib.fetchnames('*',ringing.nbells_min,ringing.nbells_max)
        self.selector=ScrollListBox(self.frame_form,40,20,self.eng.objects['m01'].name,names)
        self.selector.pack()

    ### action_ok: load method and ring it

    def action_ok(self):
        name=self.selector.get()
        self.parent.enginecmd('method m01 "%s"' %name)
        self.parent.form_method.set(name)
        self.parent.action_diagram()
        self.root.destroy()


######################################################################
### Class: TowerSelectWindow
######################################################################

class TowerSelectWindow(PopupWindow):

    ### init: create config window with selector

    def __init__(self,parent):
        PopupWindow.__init__(self,parent,'Select Tower',cancel=True)
        names=[t[0] for t in self.eng.crelib.fetchtowers('*')]
        self.selector=ScrollListBox(self.frame_form,20,5,self.eng.objects['t01'].name,names)
        self.selector.pack()

    ### action_ok: select tower

    def action_ok(self):
        name=self.selector.get()
        self.parent.enginecmd('tower t01 "%s"' %name)
        #self.parent.form_tower.set(name)
        self.root.destroy()


######################################################################
### Class: ExportWindow
######################################################################

class ExportWindow(PopupWindow):

    ### init

    def __init__(self,parent):

        # create base object
        PopupWindow.__init__(self,parent,'Export to File',cancel=True)

        # formats
        self.formats=[
            ('ASCII Text','txt')
            , ('Comma separated value (CSV)','csv')
            , ('HTML (SVG)','html')
            , ('Postscript (page)','ps')
            , ('Postscript (encapsulated image)','eps')
            , ('PDF (page)','pdf')
            , ('PNG Image','png')
            ]

        # widgets to be placed on form
        self.form_exportsfile=EntryView(self.frame_form,250,self.eng.vars['ui_export_file'])
        button_select=Button(self.frame_form,text='Select',command=self.action_select)
        outformat=os.path.splitext(self.eng.vars['ui_export_file'])[1][1:].lower()
        self.form_outformat=RadioButtonSet(self.frame_form,outformat,self.formats)
        self.form_nleads=EntryEdit(self.frame_form,3,self.eng.vars['nleads'])

        # place widgets on form
        add_to_grid(self.frame_form,[
                (0,0,True,'File Name')
                , (0,1,False,self.form_exportsfile)
                , (0,2,False,button_select)
                , (1,0,True,'Output Format')
                , (1,1,False,self.form_outformat)
                , (2,0,True,'Leads per column')
                , (2,1,False,self.form_nleads)])


    ### action_select

    def action_select(self):

        # get initial directory, filename and extension from form
        initialdir=os.path.dirname(self.form_exportsfile.get())
        initialfile=os.path.basename(os.path.splitext(self.form_exportsfile.get())[0])
        defaultextension='.'+self.form_outformat.get()

        # get filename from browser
        newfilename=asksaveasfilename(
            parent=self.root
            ,title='Export block as'
            ,defaultextension=defaultextension
            ,initialdir=initialdir
            ,initialfile=initialfile
            )

        # refresh menu - tkFileDialog sometimes locks it
        self.parent.refresh_menus()

        # stop if save is cancelled
        if newfilename=='':
            return

        # update form
        self.form_exportsfile.set(newfilename)
        self.form_outformat.set(os.path.splitext(newfilename)[1][1:])


    ### action_ok

    def action_ok(self):

        # only accept new leads per column if valid
        nleads=self.form_nleads.get()
        if nleads.isdigit() and int(nleads)>1:
            self.eng.vars['nleads']=nleads

        # get output format
        outformat=self.form_outformat.get()

        # get filename - ensure correct extension is used
        filename=os.path.splitext(self.form_exportsfile.get())[0]+'.'+outformat
        self.eng.vars['ui_export_file']=filename

        # save file
        if self.parent.enginecmd('print b01 "%s"' %filename)==0:
            showinfo('Bell View','Saved to file "%s"' %filename)

        # close window
        self.root.destroy()
            

######################################################################
### Class: ConfigWindow
######################################################################

class ConfigWindow(PopupWindow):

    ### initialise class instance

    def __init__(self,parent):

        # create object
        PopupWindow.__init__(self,parent,'Configuration',cancel=True)

        # sound engines
        sounds=[
            ('Sound off','none')
            , ('Winsound (Windows Only)','winsound')
            , ('NSSound (Mac OS X only)','nssound')
            , ('Playsound (Windows/Mac)','playsound')
            , ('PyGame (cross platform)','pygame')]

        # create widgets for form
        self.form_volumes=EntryEdit(self.frame_form,25,self.eng.vars['volumes'])
        self.form_gspath=EntryEdit(self.frame_form,25,self.eng.vars['gspath'])
        self.form_sound=RadioButtonSet(self.frame_form,self.eng.vars['sound'],sounds)

        # add widgets to form
        add_to_grid(self.frame_form, [
                (0,0,True,'Method Volumes')
                , (0,1,False,self.form_volumes)
                , (1,0,True,'Ghostscript Path')
                , (1,1,False,self.form_gspath)
                , (2,0,True,'Sound Module')
                , (2,1,False,self.form_sound)
                , (3,0,True,' ')])

        # footnote
        footnote='Please restart bellview if changing the sound module'
        Label(self.frame_form,text=footnote).grid(row=4,column=0,columnspan=2)


    ### OK button

    def action_ok(self):
        self.eng.vars['volumes']=self.form_volumes.get()
        self.eng.vars['gspath']=self.form_gspath.get()
        self.eng.vars['sound']=self.form_sound.get()
        self.root.destroy()



######################################################################
### Class: DisplayOptionsWindow
######################################################################

class DisplayOptionsWindow(PopupWindow):

    ### init: create window

    def __init__(self,parent):

        # create object
        PopupWindow.__init__(self,parent,'Display Options',cancel=True)

        # widget dictionaries
        self.form_bells={}
        self.form_weights={}
        self.form_colours={}
        self.form_vars={}
        rb_fine={}
        rb_medium={}
        rb_bold={}

        # content for grid
        grid_content=[]

        # list of keys of traces: all bell numbers + "rule"
        self.keys=[]
        self.keys.append('R')
        self.keys.extend(list(ringing.bell_symbols))

        # create widgets
        for r,b in enumerate(self.keys):

            # checkbox to enable tracing to be turned on/off
            # for each bell - does not apply to rules
            if b!='R':
                s='on' if b in self.eng.vars['tracebells'].upper() else 'off'
                self.form_bells[b]=CheckBox(self.frame_form,b,s)
                grid_content.append((r,0,False,self.form_bells[b]))
            else:
                grid_content.append((r,0,True,'Rules'))

            # trace line weights - radio buttons
            self.form_weights[b]=StringVar()
            self.form_weights[b].set(self.eng.vars.get('weight'+b,'medium'))
            rb_fine[b]=Radiobutton(self.frame_form,text='Fine',variable=self.form_weights[b],value='fine')
            rb_medium[b]=Radiobutton(self.frame_form,text='Medium',variable=self.form_weights[b],value='medium')
            rb_bold[b]=Radiobutton(self.frame_form,text='Bold',variable=self.form_weights[b],value='bold')
            grid_content.append((r,1,False,rb_fine[b]))
            grid_content.append((r,2,False,rb_medium[b]))
            grid_content.append((r,3,False,rb_bold[b]))

            # colour selectors - uses new class "GridColour"
            self.form_colours[b]=ColourSquare(
                self.frame_form
                ,hexcolour(self.eng.vars.get('colour'+b,'black'))
                ,parent
                )
            grid_content.append((r,4,False,self.form_colours[b]))

        # add margin between trace selectors and other options
        grid_content.append((0,5,True,' '))

        # variables to be controlled by checkboxes
        self.checkvars=[
            ('skel','Suppress Bell Numbers')
            ,('showcall','Show Calling Positions')
            ,('showpn','Show Place Notation')
            ,('showrule','Show Rules')
            ,('rulebefore','Rules before Lead Ends')
            ]

        # create checkbox widgets
        self.form_vars={}
        for r,n in enumerate(self.checkvars):
            self.form_vars[n[0]]=CheckBox(
                self.frame_form,n[1],self.eng.vars[n[0]])
            grid_content.append((r,6,False,self.form_vars[n[0]]))

        # add content to grid
        add_to_grid(self.frame_form,grid_content,pady=1)


    ### action_ok: action selections and refresh canvas

    def action_ok(self):

        # reset tracebells
        self.eng.vars['tracebells']=''

        # set tracebells and traces from widgets
        for b in self.keys:
            if b!='R' and self.form_bells[b].get()=='on':
                self.eng.vars['tracebells']+=b
            self.eng.vars['colour'+b]=self.form_colours[b].get()
            self.eng.vars['weight'+b]=self.form_weights[b].get()

        # set variables from checkboxes
        for n,l in self.checkvars:
            self.eng.vars[n]=self.form_vars[n].get()

        # update canvas
        self.parent.action_update()

        # close window
        self.root.destroy()

