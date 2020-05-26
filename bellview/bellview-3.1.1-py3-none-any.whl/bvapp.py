######################################################################
### Bell View
### Copyright (c) 2020 Jonathan Wilson
### Please refer to help/licence.txt for further information
### File: bvapp.py
### Description: Bell View GUI Application
### Last Modified: 26 May 2020
######################################################################

### import modules

import os
import sys
import getopt
import webbrowser
from time import sleep
from crengine import ringing
from crengine.rowfmt import linethickness, hexcolour
from crengine import Engine, CREError
from sqlite3 import IntegrityError
from .bvtk import *
from .bvwidget import *
from .bvpopup import *



######################################################################
### Class: BellViewApp
######################################################################

class BellViewApp():

    '''\
The BellViewApp class defines the Bell View application - a simple
graphical user interface for the Change Ringing Engine. It may be
run standalone, using the run_app() method, or be invoked by
another application.'''

    ### __init__ - initialise class instance

    def __init__(self):

        # package directory
        self.pkgdir=os.path.dirname(os.path.realpath(__file__))

        # engine object
        self.eng=Engine()

        # variable init file
        self.init_vars=os.path.join(self.eng.libdir,'bellview_vars.rc')

        # object init file
        self.init_objs=os.path.join(self.eng.libdir,'bellview_objs.rc')

        # log file
        self.logfile=os.path.join(self.eng.libdir,'bellview.log')

        # isringing - set if currently ringing
        self.isringing=False

        # windows - to be created later
        self.root=None
        self.popup=None


    ### __str__ = program version

    def __str__(self):

        s='%s\n\nCopyright (c) %s %s\n\nVersion %s %s on Python %s %s\n\n' %(
            self.info['fullname'].upper()
            , self.info['year']
            , self.info['author']
            , self.info['version']
            , self.info['release']
            , sys.version.partition(' ')[0]
            , sys.platform)

        s+=self.non_warranty
        s+='\n\nPlease visit %s for updates' %self.info['url']

        return s


    ### run_app - run application

    def run_app(self,argv=[]):

        '''Run the Bell View application'''

        try:

            # state
            state=0

            # get command line options
            opts,args=getopt.getopt(argv,'bdhlvzs:t:m:')

            # switches
            switches=[a for (a,b) in opts if b=='']

            # print help and exit (-h)
            if '-h' in switches:
                print('\n%s\n' %self.help_usage)
                state=1
                return state

            # print version and exit (-v)
            if '-v' in switches:
                print('\n%s\n' %self)
                state=2
                return state

            # print licence and exit (-l)
            if '-l' in switches:
                self.eng.viewhelp('licence.txt')
                state=3
                return state

            # make shortcut and exit (-z)
            if '-z' in switches:
                self.eng.makeshortcut(self,pyw=True)
                state=11
                return state

            # Redirect all output to log file
            self.eng.do_writeto(self.logfile)

            # load variables
            if os.path.isfile(self.init_vars):
                self.eng.do_input(self.init_vars)

            # process command running options (-t, -m, -s)
            for opt in opts:

                # -t = select sound engine
                if opt[0]=='-t':
                    self.eng.do_set('sound "%s"' %opt[1])

                # -m = select method volumes
                elif opt[0]=='-m':
                    self.eng.do_set('volumes "%s"' %opt[1])

                # -s = set variable
                elif opt[0]=='-s':
                    self.eng.do_set(opt[1].replace('=',' '))

            # set up method library (-d forces rebuild)
            self.eng.setup_library('-d' in switches)

            # set up sound
            self.eng.setup_sound()

            # load objects
            if os.path.isfile(self.init_objs):
                self.eng.do_input(self.init_objs)

            # if no method is defined, use Plain Hunt on 5 as default
            if 'm01' not in self.eng.objects.keys():
                self.eng.onecmd('method m01 "Plain Hunt" "5" "&5.1.5.1.5,1" "0" "" ""')

            # if no tower defined, use "Default"
            if 't01' not in self.eng.objects.keys():
                self.eng.onecmd('tower t01 Default')

        # Trap CTRL-C
        except KeyboardInterrupt:
            print('Interrupted')
            state=4

        # CRE Errors
        except CREError as msg:
            print('Error: %s' %msg)
            state=5

        # Option errors
        except getopt.GetoptError as msg:
            print('Error: %s' %msg)
            state=6

        # File errors
        except IOError as msg:
            print('Error: %s' %msg)
            state=7

        # SQLite errors
        except IntegrityError as msg:
            print('Error: Can\'t load data, possibly contains duplicates')
            state=10

        # Clean up if an error was thrown
        finally:
            if state>0:
                self.eng.clearstack()
                if self.eng.outfile is not None:
                    self.eng.outfile.close()
                    self.eng.outfile=None
                    self.eng.message('Writing to terminal')
                    return state

        # set up interface
        self.create_root_window()

        # form widgets
        self.form_method.set(self.eng.objects['m01'].name)
        self.form_mode.set(self.eng.vars['ui_current_mode'])
        self.form_touch.delete(0,END)
        self.form_touch.insert(0,self.eng.vars['ui_current_touch'])
        self.form_options.set('repeat',self.eng.vars['ui_repeat'])
        self.form_options.set('cover',self.eng.vars['cover'])
        self.form_options.set('strike',self.eng.vars['strike'])

        # ring and display
        self.action_diagram()

        # open log file hand control over to Tk
        try:
            self.root.mainloop()

        # trap Ctrl-C
        except KeyboardInterrupt:
            print('Interrupted - Exiting program')

        # save variables and objects
        self.eng.do_saveobjects(self.init_objs)
        self.eng.do_savevars(self.init_vars)

        # close logfile
        if self.eng.outfile is not None:
            self.eng.outfile.close()
            self.eng.outfile=None

        # return
        return state


    ### create_root_window - create root window

    def create_root_window(self):

        # root window
        self.root=Tk()
        self.root.title(self.info['name'])
        self.root.lift()

        # add menu
        self.menubar=Menu(self.root)
        self.root.config(menu=self.menubar)
        self.menu_names=[]
        self.menus={}
        self.add_menu('File',[
                ('Export to File...',self.action_export)
                ,('Exit',self.action_exit)
                ])
        self.add_menu('Ringing',[
                ('Diagram',self.action_diagram)
                ,('Start Ringing',self.action_start)
                ,('Stop Ringing',self.action_stop)
                ])
        self.add_menu('Options',[
                ('Select Method',self.action_method)
                ,('Select Tower',self.action_tower)
                ,('Display Options',self.action_displayopt)
                ,('Configuration',self.action_config)
                ,('Rebuild Library',self.action_dbcreate)
                ])
        self.add_menu('About',[
                ('About %s' %self.info['name'],self.action_about)
                ,('Licence',self.action_licence)
                ,('Help',self.action_help)
                ,('%s Website' %self.info['name'],self.action_homepage)
                ])


        # create frame layout

        # main frame
        frame_main=Frame(self.root)
        frame_main.pack(expand=True, fill=BOTH)

        # top frame (control form and canvas)
        frame_top=Frame(frame_main)
        frame_top.pack(expand=True, fill=BOTH, side=TOP, anchor=NW)

        # control form frame
        frame_control=Frame(frame_top)
        frame_control.pack(side=LEFT, anchor=NW, padx=10, pady=10)

        # banner
        self.banner_info(frame_control).grid(row=0,column=0,columnspan=3)

        # widgets to be placed in control form

        button_method=Button(frame_control,text='Select',command=self.action_method)
        self.form_method=EntryView(frame_control,200,'')
        self.form_mode=RadioButtonSet(frame_control,'p',[('Plain Course','p'),('Touch','t')])
        self.form_touch=EntryEdit(frame_control,20,'')
        self.form_options=CheckBoxSet(frame_control,[
                ('repeat','Repeat Touch')
                , ('cover','Tenor Behind')
                , ('strike','Bell Sound')])

        # place widgets in control form
        add_to_grid(frame_control,[
                (1,0,True,' ')
                , (2,0,True,'Method')
                , (2,1,False,self.form_method)
                , (2,2,False,button_method)
                , (3,0,True,'Ringing')
                , (3,1,False,self.form_mode)
                , (4,0,True,'Touch')
                , (4,1,False,self.form_touch)
                , (5,0,True,'Options')
                , (5,1,False,self.form_options)
                ])

        # canvas form frame
        frame_canvas=Frame(frame_top)
        frame_canvas.pack(side=RIGHT, anchor=NW, padx=10, pady=10, expand=True, fill=BOTH)
        self.canvas=Canvas(frame_canvas,width=300, height=400, scrollregion=(0,0,300,1200))
        f2vb=Scrollbar(frame_canvas,orient=VERTICAL)
        f2vb.pack(side=RIGHT, fill=Y)
        f2vb.config(command=self.canvas.yview)
        self.canvas.config(yscrollcommand=f2vb.set)
        self.canvas.pack(side=LEFT, expand=True, fill=BOTH)

        # bottom frame
        frame_button=ButtonBar(frame_main,[
                ('Diagram',self.action_diagram)
                , ('Start',self.action_start)
                , ('Stop',self.action_stop)
                , ('Display',self.action_displayopt)
                , ('Export',self.action_export)
                , ('Exit',self.action_exit)],5)
        frame_button.pack(expand=False,fill=X, side=BOTTOM, anchor=NW, padx=10, pady=10)


    ### action_exit: exit application

    def action_exit(self):
        msg='Do you want to really exit %s?' %self.info['name']
        self.action_stop()
        reply=askyesno('Exit %s' %self.info['name'],msg,default='no')
        self.refresh_menus()
        if reply:
            self.root.destroy()


    ### action_about

    def action_about(self):
        if self.is_popup():
            return
        self.action_stop()
        self.popup=AboutWindow(self)

    ### action_licence

    def action_licence(self):
        if self.is_popup(): return
        self.action_stop()
        with open(os.path.join(self.pkgdir,'help','licence.txt'),'r') as f:
            text=f.read()
            self.popup=MessageWindow(self,'Bell View and Change Ringing Engine Licence',text)


    ### action_info

    def action_info(self):
        print(self.canvas.winfo_width(),self.canvas.winfo_height())
        print(self.canvas.canvasx(0),self.canvas.canvasy(0))
        print(self.canvas.canvasx(0),self.canvas.canvasy(200))

    ### action_help

    def action_help(self):
        if self.is_popup(): return
        self.action_stop()
        with open(os.path.join(self.pkgdir,'help','help.txt'),'r') as f:
            text=f.read()
            self.popup=MessageWindow(self,'Bell View Help',text)

    ###  action_homepage: open up home page in web browser

    def action_homepage(self):
        webbrowser.get().open('https://'+self.info['url'])


    ### action_dbcreate: create methods database

    def action_dbcreate(self):
        if self.is_popup(): return
        self.action_stop()
        msg='Really rebuild library?'
        reply=askyesno('Rebuild Library',msg,default='no')
        self.refresh_menus()
        if reply:
            self.enginecmd('makelibrary')

    ### action_tower: open method selector window

    def action_tower(self):
        self.action_popup(TowerSelectWindow)

    ### action_method: open method selector window

    def action_method(self):
        self.action_popup(MethodSelectWindow)

    ### action_export: Export block to a file

    def action_export(self):
        self.action_popup(ExportWindow)


    ### action_displayopt: open trace selector window

    def action_displayopt(self):
        self.action_popup(DisplayOptionsWindow)

    ### action_config: open trace selector window

    def action_config(self):
        self.action_popup(ConfigWindow)

    ### action_popup: display a popup window

    def action_popup(self,window):
        if self.is_popup(): return
        self.action_stop()
        self.popup=window(self)


    ### action_diagram: display method

    def action_diagram(self):
        self.action_stop()
        self.eng.vars['ui_current_mode']=self.form_mode.get()
        self.eng.vars['ui_current_touch']=self.form_touch.get()
        self.eng.vars['ui_repeat']=self.form_options.get('repeat')
        self.eng.vars['cover']=self.form_options.get('cover')
        self.eng.vars['strike']=self.form_options.get('strike')
        self.ring_method()
        self.action_update()

    ### action_update: update display

    def action_update(self):
        self.action_stop()
        self.display_ring_block(False)

    ### action_start: start ringing

    def action_start(self):
        if self.isringing:
            self.isringing=False
            sleep(2)
        self.isringing=True
        self.eng.vars['ui_current_mode']=self.form_mode.get()
        self.eng.vars['ui_current_touch']=self.form_touch.get()
        self.eng.vars['ui_repeat']=self.form_options.get('repeat')
        self.eng.vars['cover']=self.form_options.get('cover')
        self.eng.vars['strike']=self.form_options.get('strike')
        self.ring_method()
        self.display_ring_block(True)

    ### action_stop: stop ringing

    def action_stop(self):
        self.isringing=False

    ### is_popup: check for an active popup

    def is_popup(self):
        s=False
        if self.popup is not None:
            if self.popup.isopen():
                self.popup.lift()
                s=True
        return s

    ### ring_method - ring method

    def ring_method(self):

        # get parameters from method
        method=self.eng.objects['m01']
        title=method.name
        nbells=method.nbells
        leadlen=method.leadlen
        
        # get variables
        vars=self.eng.vars
        mode=vars['ui_current_mode']
        touch=vars['ui_current_touch']
        repeat=vars['ui_repeat']

        # set up block
        self.enginecmd('block b01 "%s" %d %s' %(title,nbells,leadlen))

        # ring plaincourse or touch
        if mode=='t':
            self.enginecmd('touch b01 m01 "%s"' %touch)
        else:
            self.enginecmd('plaincourse b01 m01')

        # repeat touch
        if repeat=='on':
            self.enginecmd('repeat b01')


    ### display_ring_block - display or ring block on canvas

    def display_ring_block(self,ringblock):

        # objects
        vars=self.eng.vars
        block=self.eng.objects['b01']
        tower=self.eng.objects['t01']

        # cover only if there are sufficient bells
        cover=ringing.getboolean(vars['cover']) and block.nbells<ringing.nbells_max

        # number of bells (including cover)
        nbells=block.nbells+int(cover)

        # timing for ringing
        openlead=not(ringing.getboolean(vars['cartwheel']))
        gap=int(vars['pealtime'])/(42.0*(2*nbells+int(openlead)))

        # formatting variables from environment
        tracebells=vars['tracebells'].upper()
        showrule=ringing.getboolean(vars['showrule'])
        rulebefore=ringing.getboolean(vars['rulebefore'])
        skel=ringing.getboolean(vars['skel'])
        showcall=ringing.getboolean(vars['showcall'])
        showpn=ringing.getboolean(vars['showpn'])

        # other formatting variables
        fontsize=18
        fontname='Arial'
        nrows=block.len+1
        linesep=fontsize*12/10
        colsep=fontsize
        leftmargin=colsep*2
        topmargin=linesep
        ruleoffset=0

        # colours and line widths
        colours={}
        widths={}
        for b in tracebells:
            colours[b]=hexcolour(vars.get('colour'+b,'black'))
            widths[b]=linethickness(vars.get('weight'+b,'medium'),fontsize)

        # rule colour and width
        rulecolour=hexcolour(vars['colourR'])
        rulewidth=linethickness(vars['weightR'],fontsize)

        # If ringing and sound is configured, turn sound on
        # TBD - need to show failure message on GUI
        strike=False
        if ringblock and vars['strike']=='on':
            if nbells in tower.bellmaps.keys():
                tower.set(gap,cover,openlead,False)
                strike=True
            else:
                print('Too few bells to ring')

        # resize canvas if necessary
        self.canvas.config(scrollregion=(0,0,300,topmargin+linesep*nrows))
        self.canvas.delete('all')
        self.canvas.update()

        # get visible height of canvas
        # can change if window is resized
        canvheight=self.canvas.winfo_height()

        # scroll to top for ringing mode
        if ringblock:
            self.canvas.yview_moveto(0)

        # print rows

        for r in range(0,nrows):

            # bail out if stop has been pressed
            if ringblock and not(self.isringing):
                break

            # rule before leadend
            if showrule and rulebefore and block.rows[r].leadend and r>0:
                self.canvas.create_line(
                    leftmargin-0.5*colsep
                    , topmargin+(r-0.5)*linesep
                    , leftmargin+(nbells-0.5)*colsep
                    , topmargin+(r-0.5)*linesep
                    , fill='#'+rulecolour
                    , width=rulewidth
                    )

            # call marker
            if showcall and block.rows[r].call in ('-','S'):
                self.canvas.create_text(
                    leftmargin-colsep
                    , topmargin+r*linesep
                    , font=(fontname,fontsize)
                    , text=block.rows[r].call
                    )

            # row
            if not(skel):
                current=block.rows[r].places[1:]+list(range(block.nbells+1,nbells+1))
                for c in range(0,nbells):
                    self.canvas.create_text(
                        leftmargin+c*colsep
                        , topmargin+r*linesep
                        , font=(fontname,fontsize)
                        , text=ringing.bellsymbol(current[c])
                        )

            # place notation
            if showpn:
                self.canvas.create_text(
                    leftmargin+(nbells+1)*colsep
                    , topmargin+r*linesep
                    , font=(fontname,fontsize)
                    , text=block.rows[r].pn
                    , anchor=W
                    )

            # print traces
            for b in tracebells:
                n=ringing.bellnumber(b)

                if n<=block.nbells and r>0:
                    s=block.rows[r-1].places[1:].index(n)
                    t=block.rows[r].places[1:].index(n)
                    self.canvas.create_line(
                        leftmargin+s*colsep
                        , topmargin+(r-1)*linesep
                        , leftmargin+t*colsep
                        , topmargin+r*linesep
                        , fill='#'+colours[b]
                        , width=widths[b]
                        )

            # ring row
            if ringblock:
                if topmargin+r*linesep>canvheight:
                    scrollfrac=float(topmargin+r*linesep-canvheight)/float(
                        topmargin+nrows*linesep-canvheight)
                    self.canvas.yview_moveto(scrollfrac)
                self.canvas.update()
                if strike:
                    tower.rowstrike(block.rows[r])
                else:
                    sleep(1.5)

            # rule after leadend
            if showrule and not(rulebefore) and block.rows[r].leadend and r<block.len-1:
                self.canvas.create_line(
                    leftmargin-0.5*colsep
                    , topmargin+(r+0.5)*linesep
                    , leftmargin+(nbells-0.5)*colsep
                    , topmargin+(r+0.5)*linesep
                    , fill='#'+rulecolour
                    , width=rulewidth
                    )

        # stop ringing
        self.isringing=False


    ### add menu

    def add_menu(self,name,items):
        self.menu_names.append(name)
        self.menus[name]=Menu(self.menubar)
        self.menubar.add_cascade(label=name,menu=self.menus[name])
        for (label,command) in items:
            self.menus[name].add_command(label=label,command=command)

    ### refresh_menus

    def refresh_menus(self):
        for m in self.menu_names:
            self.menubar.delete(m)
        for m in self.menu_names:
            self.menubar.add_cascade(label=m, menu=self.menus[m])

    ### enginecmd - run a command on change ringing engine

    def enginecmd(self,cmds):

        try:
            for cmd in cmds.strip().split('\n'):
                self.eng.onecmd(cmd)
                r=0

        except CREError as msg:
            showerror('Bell View',msg)
            r=1

        except IOError as msg:
            showerror('Bell View',msg)
            r=2

        return r


    ### banner_info: Display banner with program info

    def banner_info(self,frame,verbose=False):
        content=[]
        content.append('Copyright (c) %s %s' %(
                self.info['year'],self.info['author']))
        if verbose:
            content.append('Version %s (%s)' %(
                    self.info['version'],self.info['release']))
            content.append('Running on Python %s (%s)' %(
                    sys.version.partition(' ')[0],sys.platform))
        content.append(self.eng.soundstat)
        return Banner(frame,self.info['fullname'],content)

    ### constant class variables

    # info: program metadata
    info={
        'name': 'Bell View'
        , 'fullname': 'Bell View Ringing Engine'
        , 'author': 'Jonathan Wilson'
        , 'year': '2020'
        , 'version': '3.1.1'
        , 'release': '26 May 2020'
        , 'url': 'www.harrogatebellringers.org/bellview'
        }

    # shortcut: content for shortcut script
    shortcut='''\
from sys import argv, exit
from bellview import BellViewApp
r=BellViewApp().run_app(argv[1:])
exit(r)
'''

    # non_warranty
    non_warranty='''\
This program comes with ABSOLUTELY NO WARRANTY. This is free software,
and you are welcome to redistribute it under certain conditions;
click on Help, Licence for details.'''

    ### help_usage: help usage message (-h)
    help_usage='''\
USAGE

    python -m bellview [OPTION] ... [OPTION]

OPTIONS

    -d          Force rebuilding of the method library
    -h          Display this message and exit
    -l          Display the licence and exit
    -v          Display version information and exit
    -z          Create desktop shortcut and exit

    -m VOLUMES  Select method volumes
    -s VAR=VAL  Set a CRE variable
    -t MODULE   Select sound module
'''


