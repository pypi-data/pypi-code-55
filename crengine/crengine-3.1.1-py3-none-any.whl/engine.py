######################################################################
### Change Ringing Engine
### Copyright (c) 2020 Jonathan Wilson
### Please refer to help/licence.txt for further information
### File: engine.py
### Description: Change Ringing Engine Command Shell
### Last Modified: 26 May 2020
######################################################################

### import modules

import sys
import os
import time
import getopt
import cmd
import csv
import pickle
import shutil
from . import crelib
from . import ringing
from . import rowset
from . import rowfmt
from . import postscript
from . import svg
from . import htmldoc
from . import bellsound
from sqlite3 import IntegrityError
from .easter import easter


######################################################################
### Class: CREError
######################################################################

class CREError(Exception):
    pass


######################################################################
### Class: Engine
######################################################################

class Engine(cmd.Cmd):

    '''\
The Engine class defines the command line interpreter for the
Change Ringing Engine. It may be run as a standalone application,
using the runengine() method, or invoked by another application.'''

    ### __init__: initialisation

    def __init__(self):

        '''\
Initialises the working environment of the Engine: working directory,
variables and objects. If the working directory (~/CRE) doesn't exist,
then a default structure is copied over. The destination of the working
directory may be changed by setting the environment variable CREROOT.'''

        cmd.Cmd.__init__(self)

        # package directory (i.e. of this file)
        self.pkgdir=os.path.dirname(os.path.realpath(__file__))

        # documentation directories
        self.helpdir=os.path.join(self.pkgdir,'help')

        # get home directory
        if sys.platform.startswith('win'):
            self.homedir=os.getenv('USERPROFILE','/')
        else:
            self.homedir=os.getenv('HOME','/')

        # root of working directory
        self.rootdir=os.path.join(self.homedir,'CRE')
        self.rootdir=os.getenv('CREROOT',self.rootdir)

        # library subdirectory
        self.libdir=os.path.join(self.rootdir,'library')

        # methods subdirectory
        self.methodsdir=os.path.join(self.rootdir,'methods')

        # towers subdirectory
        self.towersdir=os.path.join(self.rootdir,'towers')

        # defaults file
        self.initfile=os.path.join(self.libdir,'crengine.rc')

        # set shell variables to defaults
        self.vars=self.vars_default.copy()

        # set colour/weight variables for each bell
        for i,b in enumerate(ringing.bell_symbols):
            self.vars['colour%c' %b]=self.colours_default[i%len(self.colours_default)]
            self.vars['weight%c' %b]=self.weights_default[i%len(self.weights_default)]

        # platform specific settings (windows)
        if sys.platform.startswith('win'):
            self.vars.update(self.vars_win32)

        # platform specific settings (macOS a.k.a. darwin)
        elif sys.platform.startswith('darwin'):
            self.vars.update(self.vars_darwin)

        # platform specific settings (linux etc)
        elif sys.platform.startswith('linux'):
            self.vars.update(self.vars_linux)

        # apply system environment variables to CRE environment
        self.vars['pager']=os.getenv('PAGER',self.vars['pager'])
        self.vars['shell']=os.getenv('SHELL',self.vars['shell'])

        # prefix default filename settings with root working directory
        self.vars['ui_export_file']=os.path.join(self.rootdir,self.vars['ui_export_file'])

        # objects (blocks, methods, towers) - none initially
        self.objects={}

        # object stack
        self.stack=[]

        # method library - to be allocated
        self.crelib=None

        # sound package - to be set later
        self.spkg=None

        # sound status
        self.soundstat='Sound not initialised'

        # set prompt
        self.prompt='CRE> '

        # disable listing of undocumented commands
        self.undoc_header=None

        # quiet - do not print messages
        self.quiet=False

        # nesting counter for subshells (see input, run)
        self.nesting=0

        # output file for redirection
        self.outfile=None

        # error flag and error message - DEFUNCT
        self.err=False
        self.errmsg=''

        # create root working directory if non-existent
        if not(os.path.isdir(self.rootdir)):
            shutil.copytree(os.path.join(self.pkgdir,'CRE'),self.rootdir)


    ### __str__: program details

    def __str__(self):

        s='%s\n\nCopyright (c) %s %s\nVersion %s (%s) on Python %s %s\n\n' %(
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


    ### runengine: run the change ringing engine

    def runengine(self,argv=[]):

        '''\
Run the Change Ringing Engine as an interactive command interpreter.
The optional arguments are a list of options and arguments passed
from the command line.'''

        try:

            # state
            state=0

            # get command line options
            opts,args=getopt.getopt(argv,'bdhilqvze:f:o:r:s:t:m:')

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
                self.viewhelp('licence.txt')
                state=3
                return state

            # install desktop icon (-z)
            if '-z' in switches:
                self.makeshortcut(self)
                state=11
                return state

            # turn on quiet mode (-q)
            self.quiet=('-q' in switches)

            # print banner
            self.message('\n%s\n' %indent(4,str(self)))

            # input init file (unless -i is used)
            if '-i' not in switches and os.path.isfile(self.initfile):
                self.do_input(self.initfile)

            # restore a previous session (-r)
            if '-r' in dict(opts).keys():
                self.do_restore(dict(opts)['-r'])

            # Redirect if -o is used
            if '-o' in dict(opts).keys():
                self.do_writeto(dict(opts)['-o'])

            # process command running options (-e, -f, -s)
            for opt in opts:

                # -t = select sound engine
                if opt[0]=='-t':
                    self.do_set('sound "%s"' %opt[1])

                # -m = select method volumes
                elif opt[0]=='-m':
                    self.do_set('volumes "%s"' %opt[1])

                # -s = set variable
                elif opt[0]=='-s':
                    self.do_set(opt[1].replace('=',' '))

                # -e = run any command
                elif opt[0]=='-e':
                    self.onecmd(opt[1])
                    
                # -f = input file
                elif opt[0]=='-f':
                    self.do_input(opt[1])

            # set up method library (-d forces rebuild)
            self.setup_library('-d' in switches)

            # set up sound
            self.setup_sound()

            # run files supplied as arguments
            for arg in args:
                self.do_run(arg)

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

        # Deserialisation errors
        except pickle.UnpicklingError as msg:
            print('Error: Session file in incorrect format, possibly corrupt')
            state=8
        
        # Serialisation errors
        except pickle.PicklingError as msg:
            print('Error: Can\'t save session')
            state=9

        # SQLite errors
        except IntegrityError as msg:
            print('Error: Can\'t load data, possibly contains duplicates')
            state=10

        # Close output stream
        finally:
            self.clearstack()
            if self.outfile is not None:
                self.outfile.close()
                self.outfile=None
                self.message('Writing to terminal')

        # exit if error was thrown
        if state>0:
            return state

        # exit if running in batchmode
        if '-b' in switches or len(args)>0:
            return state

        # change to root working directory
        os.chdir(self.rootdir)

        # enter interactive session:
        inloop=True
        while inloop:

            # interactive loop
            try:
                self.cmdloop()
                inloop=False

            # Trap Ctrl-C
            except KeyboardInterrupt:
                print('Interrupted')

            # CRE generated errors
            except CREError as msg:
                print('Error: %s' %msg)

            # File errors
            except IOError as msg:
                print('Error: %s' %msg)

            # Deserialisation errors
            except pickle.UnpicklingError as msg:
                print('Error: Session file in incorrect format, possibly corrupt')

            # Serialisation errors
            except pickle.PicklingError as msg:
                print('Error: Can\'t save session')

            # SQLite3 errors
            except IntegrityError as msg:
                print('Error: Can\'t load data, possibly contains duplicates')

            # clear stack and close any open output stream
            finally:
                self.clearstack()
                if self.outfile is not None:
                    self.outfile.close()
                    self.outfile=None
                    self.message('Writing to terminal')

        # end of program
        return state


    ### precmd - handles comments and blank lines

    def precmd(self,line):
        (linec,sep,comment)=line.partition('#')
        linec=linec.strip()
        if linec=='':
            linec='skip'
        return linec

    ### default - throw error if command isn't recognised

    def default(self,line):
        name=line.partition(' ')[0]
        raise CREError('Command "%s" not recognised' %name)

    ### postcmd - clear error status

    def postcmd(self,stop,line):
        return cmd.Cmd.postcmd(self,stop,line)

    ### empty - do nothing if line is empty

    def empty(self):
        pass

    ### print_topics - disable printing undocumented commands

    def print_topics(self,header,cmds,cmdlen,maxcol):
        if header is not None:
            cmd.Cmd.print_topics(self,header,cmds,cmdlen,maxcol)

    ### skip - dummy command to enable validation
    ### errors to bypass command execution

    def do_skip(self,line):
        pass

    ### appendto - redirect output to a filestream

    def do_appendto(self,line):
        args=self.splitline(line,0,['string'])

        # close existing filestream
        if self.outfile is not None:
            self.outfile.close()
            self.outfile=None

        # open new filestream
        if len(args)>0:
            filename=args[0]
            self.outfile=open(filename,'a')
            self.message('Writing to "%s"' %filename)
        else:
            self.message('Writing to screen')

    def help_appendto(self):
        self.viewhelp('system.html')


    ### block - define a new block

    def do_block(self,line):

        # read arguments
        args=self.splitline(line,3,['objname','string','nbells','number1'])

        # block identifier
        b=args[0]

        # attributes
        name=args[1]
        nbells=int(args[2])
        leadlen=2*nbells
        if len(args)>3:
            leadlen=int(args[3])

        # create block
        block=ringing.Block(name,nbells)
        block.leadlen=leadlen

        # store as object
        if b in self.objects.keys():
            self.objects.pop(b)
        self.objects[b]=block
        self.message('Block "%s" defined' %b)

    def help_block(self):
        self.viewhelp('block.html')


    ### callchange - ring call change

    def do_callchange(self,line):

        # read arguments
        args=self.splitline(line,2,['block','callchange'])

        # block
        block=self.objects[args[0]]

        # ring changes
        for call in args[1:]:
            block.callchange(call[0],(call+'.')[2])

    def help_callchange(self):
        self.viewhelp('callchange.html')


    ### cd - change working directory

    def do_cd(self,line):
        args=self.splitline(line,0,['string'])
        cwd=args[0] if len(args)>0 else self.rootdir
        os.chdir(cwd)       

    def help_cd(self):
        self.viewhelp('system.html')


    ### chime - sound bells

    def do_chime(self,line):

        # read arguments
        args=self.splitline(line,2,['tower','string'])

        # tower object
        tower=self.objects[args[0]]

        # duration of crochet
        gap=60.0/float(self.vars['tempo'])

        # return if sound is turned off
        if self.vars['strike']=='off':
            return

        # chime bells
        for bar in args[1:]:

            # separate notes and duration
            (notes,sep,dur)=bar.partition(',')

            # no duration implies "crochet"
            if dur=='':
                dur='1.0'

            # stop if duration not a number
            if not(isdecimal(dur)):
                raise CREError('Duration "%s" not a number' %dur)

            # chime bells
            tower.chime(notes,gap*float(dur))


    def help_chime(self):
        self.viewhelp('chime.html')


    ### clear - remove all rows from a block, without deleting it

    def do_clear(self,line):
        args=self.splitline(line,1,['block'])
        self.objects[args[0]].clear()

    def help_clear(self):
        self.viewhelp('clear.html')


    ### copy - copy an object

    def do_copy(self,line):
        args=self.splitline(line,2,['object','objname'])
        self.objects[args[1]]=self.objects[args[0]].copy()
        if self.objects[args[1]].objtype in ['tower']:
            self.objects[args[1]].setbellsounds()

    def help_copy(self):
        self.viewhelp('objects.html')


    ### comment - add a comment to a block

    def do_comment(self,line):

        # read arguments
        args=self.splitline(line,3,['block','number','string'])

        # block ID and attributes
        b=args[0]
        rowno=int(args[1])
        comment=args[2]

        # block object
        block=self.objects[b]

        # check row number is in range
        if rowno>block.len:
            raise CREError('No such row %d in block "%s"' %(rowno,b))

        # add comment
        block.addcomment(rowno,comment)

    def help_comment(self):
        self.viewhelp('comment.html')


    ### makelibrary - make method library

    def do_makelibrary(self,line):
        self.setup_library(True)

    def help_makelibrary(self):
        self.viewhelp('library.html')


    ### delete - delete object

    def do_delete(self,line):
        args=self.splitline(line,1,['object'])
        self.objects.pop(args[0])

    def help_delete(self):
        self.viewhelp('objects.html')


    ### echo - print a line of text on the screen

    def do_echo(self,line):
        self.write(line)

    def help_echo(self):
        self.viewhelp('echo.html')

    def do_easter(self,line):
        args=self.splitline(line,0,['number'])
        year=int(args[0]) if len(args)>0 else 0
        print('Plain hunting for easter eggs?')
        print('Easter Sunday is',easter(year).strftime('%A %d %B %Y'))

    ### input - read and execute commands from a file

    def do_input(self,line):

        # read arguments
        args=self.splitline(line,1,['string'])

        # prevent too many levels of nesting
        if self.nesting>10:
            raise CREError('Too many levels of nesting')

        # get filename
        filename=args[0]

        # read file
        with open(filename,'r') as fp:
            lines=fp.read().splitlines()

        # execute line by line
        self.nesting+=1
        for line in lines:
            linec=self.precmd(line)
            self.onecmd(linec)
        self.nesting-=1


    def help_input(self):
        self.viewhelp('run.html')

    ### listmethods - list all methods in library

    def do_listmethods(self,line):
        args=self.splitline(line,0,['string','nbells'])
        key=args[0] if len(args)>0 else '*'
        nmin=int(args[1]) if len(args)>1 else ringing.nbells_min
        nmax=int(args[1]) if len(args)>1 else ringing.nbells_max
        names=self.crelib.fetchnames(key,nmin,nmax)
        self.write('\n'.join(names))

    def help_listmethods(self):
        self.viewhelp('library.html')


    ### method - define a method

    def do_method(self,line):

        # read arguments
        args=self.splitline(line,2,['objname','string','nbells','string','numberpm','string','string'])

        # method ID
        m=args[0]

        # place notation argument given:
        # define method from command line

        if len(args)>3:

            # set method attributes
            basename=ringing.splitmethodname(args[1])[0]
            nbells=int(args[2])
            pn=args[3]
            callpos=int(args[4]) if len(args)>4 else 0
            bobpn=args[5] if len(args)>5 else ''
            singlepn=args[6] if len(args)>6 else ''

        # No place notation argument:
        # attempt to look up method in database

        else:

            # lookup key
            key=args[1]

            # if nbells argument is given, restrict search
            if len(args)>2:
                nmin=int(args[2])
                nmax=nmin
                ndesc=' %d bell' %nmin

            # otherwise allow search for all numbers of bells
            else:
                nmin=ringing.nbells_min
                nmax=ringing.nbells_max
                ndesc=''

            # look up method in database
            # name is a wildcard
            names=self.crelib.fetchnames(key,nmin,nmax)

            # nothing found
            if len(names)==0:
                raise CREError('No%s method matching "%s"' %(ndesc,key))

            # not a unique match
            if len(names)>1:
                raise CREError('More than one%s method matching "%s"\n%s' %(
                        ndesc,key,'\n'.join(names)))

            # unique match - get attributes
            results=self.crelib.fetchmethod(names[0])

            # exit if unique match lookup fails - it shouldn't
            if len(results)==0:
                raise CREError('Method "%s" not found' %names[0])

            # set method attributes
            basename=str(results[0][0])
            nbells=int(str(results[0][1]))
            pn=str(results[0][2])
            callpos=int(str(results[0][3]))
            bobpn=str(results[0][4])
            singlepn=str(results[0][5])

        # define method
        method=ringing.Method(basename,nbells)
        method.setmethod(pn)

        # define call
        method.setcalls(callpos,bobpn,singlepn)

        # store as object
        if m in self.objects.keys():
            self.objects.pop(m)
        self.objects[m]=method
        self.message('Method "%s" defined: %s' %(m,method))

    def help_method(self):
        self.viewhelp('method.html')

    ### savevars - save global variables to script

    def do_savevars(self,line):
        args=self.splitline(line,1,['string'])
        filename=args[0]
        with open(filename,'w') as fp:
            for name in sorted(self.vars.keys()):
                fp.write('set %s "%s"\n' %(name,self.vars[name]))
        self.message('Variables saved to "%s"' %filename)

    def help_savevars(self):
        self.viewhelp('output.html')

    ### saveobjects - save objects to script

    def do_saveobjects(self,line):
        args=self.splitline(line,1,['string'])
        filename=args[0]
        with open(filename,'w') as fp:
            for x in sorted(self.objects.keys()):
                fp.write('%s %s %s\n' %(self.objects[x].objtype,x,self.objects[x]))
                for v in sorted(self.objects[x].vars.keys()):
                    fp.write('set %s.%s "%s"\n' %(x,v,self.objects[x].vars[v]))
        self.message('Objects saved to "%s"' %filename)

    def help_saveobjects(self):
        self.viewhelp('output.html')


    ### plaincourse - ring a plain course

    def do_plaincourse(self,line):

        # read arguments
        args=self.splitline(line,2,['block','method'])

        # block and method ID
        b=args[0]
        m=args[1]

        # block and method objects
        block=self.objects[b]
        method=self.objects[m]

        # stop if there are too few bells
        if method.nbells>block.nbells:
            raise CREError('Too few bells in block "%s" to ring method "%s"' %(b,m))

        # ring the block
        block.rang=0
        method.ringplaincourse(block)
        self.message('%d rows rang' %block.rang)

    def help_plaincourse(self):
        self.viewhelp('touch.html')


    ### plainhunt - ring plain hunt

    def do_plainhunt(self,line):

        # read arguments
        args=self.splitline(line,1,['block','number'])

        # block ID
        b=args[0]

        # block object
        block=self.objects[b]

        # number of bells
        nbells=block.nbells
        if len(args)>1:
            nbells=int(args[1])

        # stop if there are too few bells
        if nbells<2 or nbells>block.nbells:
            raise CREError('Number of bells to hunt out of range (2-%d)' %block.nbells)

        # ring plainhunt
        block.rang=0
        block.ringplainhunt(nbells)
        self.message('%d rows rang' %block.rang)

    def help_plainhunt(self):
        self.viewhelp('touch.html')


    ### plainlead - ring a plain lead in a method

    def do_plainlead(self,line):

        # read arguments
        args=self.splitline(line,2,['block','method','number'])

        # block and method ID
        b=args[0]
        m=args[1]

        # number of leads
        n=1
        if len(args)>2:
            n=int(args[2])

        # block and method objects
        block=self.objects[b]
        method=self.objects[m]

        # stop if there are too few bells
        if method.nbells>block.nbells:
            raise CREError('Too few bells in block "%s" to ring method "%s"' %(b,m))

        # ring "n" plain leads
        block.rang=0
        for i in range(0,n):
            method.ringplainlead(block)
        self.message('%d rows rang' %block.rang)

    def help_plainlead(self):
        self.viewhelp('touch.html')


    ### print - print a block

    def do_print(self,line):

        # read arguments
        args=self.splitline(line,1,['object','string'])

        # get object ID
        b=args[0]

        # object is a block - print
        if self.objects[b].objtype=='block':
            block=self.objects[b]

        # object is a method - ring plaincourse and print
        elif self.objects[b].objtype=='method':
            method=self.objects[b]
            block=ringing.Block(method.name,method.nbells)
            block.leadlen=method.leadlen
            block.vars=method.vars
            method.ringplaincourse(block)

        # other object - error
        else:
            raise CREError('Can\'t print %s object "%s"' %(self.objects[b].objtype,b))

        # exit if no rows
        if block.len==0:
            self.message('Block "%s" has no rows' %b)
            return

        # merge block vars
        vars=self.vars.copy()
        vars.update(block.vars)

        # cover
        cover=vars['cover']=='on' and block.nbells<ringing.nbells_max

        # write to stdout by default
        filename=''
        outformat='out'

        # optional 2nd argument is filename
        if len(args)>1:
            filename=args[1]
            outformat=os.path.splitext(filename)[1][1:].lower()

        # print output depending on the format (file extension)

        if outformat in ['txt','text','out'] and filename!='':

            # Text (to file)
            fmt=rowfmt.Format(block.nbells+int(cover),block.leadlen,False,False,vars['textpages']=='off')
            fmt.set(vars)
            fmt.trace(vars['traceformat'],vars)
            doc=rowset.Document(fmt,block.name)
            doc.addblock(block,block.name)
            self.writetofile(doc.typeset(),filename)

        elif outformat in ['txt','text','out'] and vars['pagerows']=='on':

            # Text output (via pager)
            # Force single column and overstrike mode
            fmt=rowfmt.Format(block.nbells+int(cover),block.leadlen,False,False,True)
            fmt.set(vars)
            fmt.trace('over',vars)
            doc=rowset.Document(fmt,block.name)
            doc.addblock(block,block.name)
            self.pageview(doc.typeset())

        elif outformat in ['txt','text','out']:

            # Text output (standard output)
            fmt=rowfmt.Format(block.nbells+int(cover),block.leadlen,False,False,vars['textpages']=='off')
            fmt.set(vars)
            fmt.trace(vars['traceformat'],vars)
            doc=rowset.Document(fmt,block.name)
            doc.addblock(block,block.name)
            self.write('')
            self.write(doc.typeset())

        elif outformat in ['csv'] and filename!='':

            # CSV - may be opened in Excel etc
            fmt=rowfmt.Format(block.nbells+int(cover),block.leadlen,False,False,True)
            fmt.set(vars)
            fmt.trace('plain',vars)
            doc=rowset.Document(fmt,block.name)
            doc.addblock(block,block.name)
            self.writetofile(doc.typesetcsv(),filename)

        elif outformat in ['htm','html','svg'] and filename!='':

            # HTML (SVG) - may be opened in web browser
            fmt=rowfmt.Format(block.nbells+int(cover),block.leadlen,True,True,False)
            fmt.set(vars)
            fmt.trace('svg',vars)
            doc=rowset.Document(fmt,block.name)
            doc.addblock(block,block.name)
            self.writetofile(svg.typeset(doc,fmt),filename)

        elif outformat in ['ps','eps'] and filename!='':

            # Postscript / Encapsulated PS
            fmt=rowfmt.Format(block.nbells+int(cover),block.leadlen,True,outformat=='eps',False)
            fmt.set(vars)
            fmt.trace('ps',vars)
            doc=rowset.Document(fmt,block.name)
            doc.addblock(block,block.name)
            self.writetofile(postscript.typeset(doc,fmt),filename)

        elif outformat in ['pdf'] and filename!='':

            # PDF
            fmt=rowfmt.Format(block.nbells+int(cover),block.leadlen,True,False,False)
            fmt.set(vars)
            fmt.trace('ps',vars)
            doc=rowset.Document(fmt,block.name)
            doc.addblock(block,block.name)
            self.writepdf(postscript.typeset(doc,fmt),filename)

        elif outformat in ['png'] and filename!='':

            # PNG
            fmt=rowfmt.Format(block.nbells+int(cover),block.leadlen,True,True,False)
            fmt.set(vars)
            fmt.trace('ps',vars)
            doc=rowset.Document(fmt,block.name)
            doc.addblock(block,block.name)
            self.writepng(postscript.typeset(doc,fmt),filename
                          ,width=fmt.pagewidth
                          ,height=fmt.pageheight)

        else:

            # Bad output format
            raise CREError('Unrecognised output format "%s"' %outformat)

        # output message
        if filename!='':
            self.message('Block "%s" written to file "%s"' %(
                    b,os.path.basename(filename)))

    def help_print(self):
        self.viewhelp('print.html')

    ### pwd - display current working directory

    def do_pwd(self,line):
        self.write(os.getcwd())

    def help_pwd(self):
        self.viewhelp('system.html')

    ### rename - rename an object

    def do_rename(self,line):
        args=self.splitline(line,2,['object','objname'])
        self.objects[args[1]]=self.objects[args[0]]
        self.objects.pop(args[0])

    def help_rename(self):
        self.viewhelp('objects.html')


    ### repeat - repeat existing rows of block as changes until rounds

    def do_repeat(self,line):
        args=self.splitline(line,1,['block'])
        block=self.objects[args[0]]
        block.rang=0
        block.repeat()
        self.message('%d rows rang' %block.rang)

    def help_repeat(self):
        self.viewhelp('touch.html')

    ### restore - restore entire session

    def do_restore(self,line):
        args=self.splitline(line,1,['string'])
        filename=args[0]

        # restore variables and objects
        with open(filename,'rb') as fp:
            self.vars=pickle.load(fp)
            self.objects=pickle.load(fp)

        # restore obj-C part of tower
        for k,obj in self.objects.items():
            if obj.objtype in ['tower']:
                obj.setbellsounds()

        self.message('Session restored from "%s"' %filename)

    def help_restore(self):
        self.viewhelp('save.html')


    ### ring - actually ring the block!!!

    def do_ring(self,line):

        # read arguments
        args=self.splitline(line,2,['object','tower'])

        # object ID
        b=args[0]

        # object is a block - print
        if self.objects[b].objtype=='block':
            block=self.objects[b]

        # object is a method - ring plaincourse and print
        elif self.objects[b].objtype=='method':
            method=self.objects[b]
            block=ringing.Block(method.name,method.nbells)
            block.leadlen=method.leadlen
            block.vars=method.vars
            method.ringplaincourse(block)

        # other object - error
        else:
            raise CREError('Can\'t ring %s object "%s"' %(self.objects[b].objtype,b))

        # tower object
        tower=self.objects[args[1]]

        # merge block vars
        vars=self.vars.copy()
        vars.update(block.vars)

        # enable covering
        cover=vars['cover']=='on' and block.nbells<ringing.nbells_max

        # repeatrow
        repeatrow=max(1,int(vars['repeatrow']))

        # open lead
        openlead=vars['cartwheel']=='off'

        # gap
        gap=int(vars['pealtime'])/(42.0*(2*block.nbells+2*int(cover)+int(openlead)))

        # set ringing attributes
        tower.set(gap,cover,openlead,True)
        
        # check for tower and exit if too few bells
        if not(tower.blockcheck(block)):
            raise CREError('Can\'t ring on %d bells with %s' %(block.nbells,b))

        # set up format - as for single column text
        fmt=rowfmt.Format(block.nbells+int(cover),block.leadlen,False,False,True)
        fmt.set(vars)
        fmt.trace(vars['traceformat'],vars)
        self.write('')

        # ring block on bells if tower is defined and sound is on
        if vars['strike']=='on':
            for row in [block.rows[0]]+block.rows:
                for i in range(0,repeatrow):
                    self.write(fmt.typesetrow(row))
                    tower.rowstrike(row)

        # otherwise ring silently
        else:
            for row in [block.rows[0]]+block.rows:
                for i in range(0,repeatrow):
                    self.write(fmt.typesetrow(row))
                    tower.nostrike(row)

        self.write('')

    def help_ring(self):
        self.viewhelp('ring.html')



    ### run - read and execute commands from a file

    def do_run(self,line):
        args=self.splitline(line,1,['string'])
        self.push()
        self.do_input(args[0])
        self.pop()

    def help_run(self):
        self.viewhelp('input.html')


    ### save - save entire session

    # N.B. Pickle doesn't work with objective-C objects (i.e. towers)
    # so will need to skip these. TBD - save a placeholder and get
    # restore to reinstate them (or perhaps package the pickled
    # file up with a command file to load the towers?)

    def do_save(self,line):

        # read arguments
        args=self.splitline(line,1,['string'])
        filename=args[0]

        # select objects for pickling
        # towers must be copied without the obj-C objects
        # or they won't pickle
        objects={}
        for k,obj in self.objects.items():
            if obj.objtype in ['tower']:
                objects[k]=obj.copy()
            else:
                objects[k]=obj

        # save to a "pickled" file
        with open(filename,'wb') as fp:
            pickle.dump(self.vars,fp)
            pickle.dump(objects,fp)
            self.message('Session saved to "%s"' %filename)

    def help_save(self):
        self.viewhelp('save.html')


    ### set - set a variable

    def do_set(self,line):

        # read arguments
        args=self.splitline(line,2,['var','string'])

        # separate object.variable
        (x,v)=varsep(args[0])

        # get validation rule and validate
        for k in self.validation_var.keys():
            if v==k or (k.endswith('*') and v.startswith(k[:-1])):
                self.validate(args[1],self.validation_var[k])

        # set variable within block
        if x!='':
            self.objects[x].vars[v]=args[1]

        # otherwise set global variable
        else:
            self.vars[v]=args[1]

    def help_set(self):
        self.viewhelp('set.html')


    ### shell - run an operating system command

    def do_shell(self,line):

        # run command (or enter shell if no arguments)
        if len(line)>0:
            rtn=os.system(line)
        else:
            rtn=os.system(self.vars['shell'])

        if rtn>0:
            self.message('System command terminated abnormally')

    def help_shell(self):
        self.viewhelp('system.html')


    ### show - display object

    def do_show(self,line):

        # read arguments
        args=self.splitline(line,0,['string'])

        # no arguments - list everything
        if len(args)<1:
            self.write('\nVariables:')
            for x in sorted(self.vars.keys()):
                self.write('%s = %s' %(x,self.vars[x]))
            for t in self.object_types:
                self.write('\n%ss:' %t.title())
                for x in self.getobjects(t):
                    self.write('%s: %s' %(x,self.objects[x].name))
            self.write('')
            return

        # get object
        x=args[0]

        # variable
        if x in self.vars.keys():
            self.write('%s = %s' %(x,self.vars[x]))

        # object
        elif x in self.objects.keys():
            self.write('\n%s "%s":\n' %(self.objects[x].objtype.title(),x))
            self.write(self.objects[x].show())

        # environment - all environment variables
        elif x in ('env'):
            self.write('\nVariables:\n')
            self.write(self.show())

        # no such object
        else:
            raise CREError('No such object "%s"' %x)

    def show(self):
        return '\n'.join(
            ['%s = %s' % (n,self.vars[n])
             for n in sorted(self.vars.keys())])

    def getobjects(self,objtype):
        return [x for x in self.objects.keys()
                if self.objects[x].objtype==objtype]

    def help_show(self):
        self.viewhelp('show.html')


    ### showcomments - list comments for block

    def do_showcomments(self,line):
        args=self.splitline(line,1,['block'])
        self.write(self.objects[args[0]].showcomments())

    def help_showcomments(self):
        self.viewhelp('comment.html')


    ### sleep - pause for a set time

    def do_sleep(self,line):
        args=self.splitline(line,1,['decimal'])
        time.sleep(float(args[0]))

    def help_sleep(self):
        self.viewhelp('sleep.html')


    ### stop - stop bells from ringing

    def do_stop(self,line):
        args=self.splitline(line,1,['tower'])
        self.objects[args[0]].stopstrike()

    def help_stop(self):
        self.viewhelp('stop.html')


    ### touch - ring a touch

    def do_touch(self,line):

        # read arguments
        args=self.splitline(line,3,['block','method','string','number'])

        # get ID's and touch string
        b=args[0]
        m=args[1]
        ts=args[2]
        n=1
        if len(args)>3:
            n=int(args[3])

        # block and method objects
        block=self.objects[b]
        method=self.objects[m]

        # stop if there are too few bells
        if method.nbells>block.nbells:
            raise CREError('Too few bells in block "%s" to ring method "%s"' %(b,m))

        # ring touch
        block.rang=0
        for i in range(0,n):
            method.ringtouch(block,ts)
        self.message('%d rows rang' %block.rang)

    def help_touch(self):
        self.viewhelp('touch.html')


    ### tower - set up bell sound

    def do_tower(self,line):

        # read arguments
        args=self.splitline(line,2,['objname','string'])

        # tower ID and name
        t=args[0]
        tkey=args[1]

        # read tower
        results=self.crelib.fetchtowers(tkey)

        # no tower found
        if len(results)<1:
            raise CREError('No tower matching "%s"' %tkey)

        # more than one tower found
        if len(results)>1:
            raise CREError('More than one tower matching "%s":\n%s' %(
                    tkey,'\n'.join([r[0] for r in results])))

        # get parameters
        name=results[0][0]
        samples=results[0][2]
        nbells=results[0][3]
        bellset=results[0][4]

        # check that bellset is large enough
        if len(bellset)<nbells:
            raise CREError('Too few bells in bell set "%s"' %bellset)

        # samples directory
        samplesdir=os.path.join(self.towersdir,results[0][2])

        # define new tower
        tower=bellsound.Tower(name,nbells,bellset,samplesdir)

        # exit if bell sample files can't be found
        if tower.missing!='':
            raise CREError('Bell samples not in %s: %s' %(samplesdir,tower.missing))

        # load sample files
        tower.setbellsounds(self.spkg)

        # apply custom bellmaps
        bellmaps=self.crelib.fetchbellmaps(name)
        for bellmap in bellmaps:
            tower.bellmaps[bellmap[1]]=bellmap[2]

        # add tower as object
        if t in self.objects.keys():
            self.objects.pop(t)
        self.objects[t]=tower
        self.message('Tower "%s" defined' %t)

    def help_tower(self):
        self.viewhelp('tower.html')


    ### unset - unset a variable

    def do_unset(self,line):

        # read arguments
        args=self.splitline(line,1,['var'])

        # separate block.var
        (x,v)=varsep(args[0])

        # trap attempt to unset a global variable
        if x=='':
            raise CREError('Can\'t unset global variable "%s"' %v)

        # remove variable from object
        if v in self.objects[x].vars.keys():
            self.objects[x].vars.pop(v)

    def help_unset(self):
        self.viewhelp('set.html')


    ### uncomment - remove a comment from a block

    def do_uncomment(self,line):

        # read arguments
        args=self.splitline(line,2,['block','number'])

        # object
        b=args[0]
        block=self.objects[b]

        # row number
        rowno=int(args[1])

        # check row number
        if rowno<0 or rowno>block.len:
            raise CREError('No such row %d in "%s"' %(rowno,b))

        # delete comment
        block.delcomment(rowno)

    def help_uncomment(self):
        self.viewhelp('comment.html')

    ### writeto - redirect output to a filestream

    def do_writeto(self,line):
        args=self.splitline(line,0,['string'])

        # close existing filestream
        if self.outfile is not None:
            self.outfile.close()
            self.outfile=None

        # open new filestream
        if len(args)>0:
            filename=args[0]
            self.outfile=open(filename,'w')
            self.message('Writing to "%s"' %filename)
        else:
            self.message('Writing to screen')

    def help_writeto(self):
        self.viewhelp('system.html')


    ### exit - exit the command shell

    def do_exit(self,line):
        return True

    def help_exit(self):
        self.viewhelp('exit.html')


    ### EOF = exit

    def do_EOF(self,line):
        return True


    ### non-command help topics

    def help_about(self):
        print('\n%s\n' %indent(4,str(self)))

    def help_licence(self):
        self.viewhelp('licence.txt')

    def help_towermap(self):
        self.viewhelp('towermap.html')

    def help_placenotation(self):
        self.viewhelp('placenotation.html')

    def help_bellview(self):
        self.viewhelp('bellview.html')

    ### viewhelp - view help page

    def viewhelp(self,name):
        content=self.formathelp(name)
        if self.vars['pagedoc']=='on':
            self.pageview(content)
        else:
            print(content)

    ### formatdoc - format documentation

    def formathelp(self,filename):

        # full pathname of file
        filename=os.path.join(self.helpdir,filename)

        # read file
        with open(filename,'r') as fp:
            content=fp.read()

        # format as HTML (see htmldoc.py)
        if os.path.splitext(filename)[1].lower() in ['.html']:
            doc=htmldoc.HTMLText()
            doc.feed(content)
            content=doc.result

        # return content
        return content


    ### pageview - view content with pager

    def pageview(self,content):
        filter=self.vars['pager'].strip()
        with os.popen(filter,'w') as fp:
            fp.write(content)

    ### writepdf - write postscript content as PDF using Ghostscript

    def writepdf(self,content,filename):

        # Ghostscript options
        # options taken from ps2pdf filter from macTeX
        gsopts=[
            '-q','-P-','-dSAFER','-dNOPAUSE','-dBATCH'
            ,'-dCompatibilityLevel=1.4'
            ,'-sDEVICE=pdfwrite'
            ,'-sPAPERSIZE=%s' %self.vars['papersize'].lower()
            ,'-sstdout=%stderr'
            ,'"-sOutputFile=%s"' %filename
            #,'-c .setpdfwrite'
            ,'-f -']

        # Ghostscript command filter
        filter='"%s" %s' %(self.vars['gspath'],' '.join(gsopts))

        # Pipe through filter
        with os.popen(filter,'w') as fp:
            fp.write(content)

    ### writepng - write postscript content as PNG using Ghostscript
    ### default image size is 595x842 (A4)

    def writepng(self,content,filename,width=595,height=842):

        # Ghostscript options
        gsopts=[
            '-q','-P-','-dSAFER','-dNOPAUSE','-dBATCH'
            ,'-r72'
            ,'-g%dx%d' %(width,height)
            ,'-sDEVICE=png16m'
            ,'-dTextAlphaBits=4'
            ,'-dGraphicsAlphaBits=4'
            ,'"-sOutputFile=%s"' %filename
            ,'-f -']

        # Ghostscript command filter
        filter='"%s" %s' %(self.vars['gspath'],' '.join(gsopts))

        # Pipe through filter
        with os.popen(filter,'w') as fp:
            fp.write(content)


    ### writetofile - write to file

    def writetofile(self,content,filename):
        with open(filename,'w') as fp:
            fp.write(content+'\n')

    ### write - write to output stream or standard output

    def write(self,content):
        if self.outfile is None:
            print(content)
        else:
            self.outfile.write(content+'\n')


    ### setup_library - set up method library

    def setup_library(self,rebuild):

        # create CRELIB object
        self.crelib=crelib.CRELib(os.path.join(self.libdir,'crelib.db'))

        # stop if database exists and no rebuild
        if not(rebuild) and self.crelib.exists():
            return

        # recreate database
        self.crelib.drop()
        self.crelib.create()
        self.crelib.initialise()

        # load in methods
        for volume in self.vars['volumes'].split(','):
            filename=os.path.join(self.methodsdir,volume.strip()+'.csv')
            n=self.crelib.loadmethods(filename)
            self.message('Loaded methods from "%s", %d methods' %(
                    os.path.basename(filename),n))

        # load towers
        n=self.crelib.loadtowers(os.path.join(self.towersdir,'tower.csv'))
        self.message('Loaded %d towers' %n)

        # load bell maps
        n=self.crelib.loadbellmaps(os.path.join(self.towersdir,'bellmap.csv'))
        self.message('Loaded %d bellmaps' %n)


    ### setup_sound - loads the sound module

    def setup_sound(self):

        try:
            self.spkg=bellsound.soundinit(self.vars['sound'])
            if self.vars['sound']!='none':
                self.soundstat='Sound (%s) enabled' %self.vars['sound']
            else:
                self.soundstat='Sound not enabled'

        except ImportError:
            self.pkg=None
            self.soundstat='Sound (%s) unavailable' %self.vars['sound']

        finally:
            self.message(self.soundstat)


    ### split command line into arguments and validate

    def splitline(self,line,narg,argtypes):

        # split line into arguments
        args=ringing.splitline(line)

        # check number of arguments
        if len(args)<narg:
            raise CREError('Too few arguments (minimum %d)' %narg)

        # validate arguments
        for n in range(0,min(len(args),len(argtypes))):
            self.validate(args[n],argtypes[n])

        # if there are more arguments than types, use the last type
        for n in range(len(argtypes),len(args)):
            self.validate(args[n],argtypes[-1])


        # return arguments
        return args


    ### validate - validate a single argument

    def validate(self,arg,vtype):

        # string - no validation
        if vtype in ['string']:
            pass

        # whole number (zero or positive)
        elif vtype in ['number']:
            if not(isnumber(arg,nmin=0)):
                raise CREError('Invalid number "%s"' %arg)

        # whole number (positive)
        elif vtype in ['number1']:
            if not(isnumber(arg,nmin=1)):
                raise CREError('Invalid number "%s"' %arg)

        # whole number (positive or negative)

        elif vtype in ['numberpm']:
            if not(isnumber(arg)):
                raise CREError('Invalid number "%s"' %arg)

        # decimal number
        elif vtype in ['decimal']:
            if not(isdecimal(arg)):
                raise CREError('Invalid decimal number "%s"' %arg)

        # nbells
        elif vtype in['nbells']:
            if not(ringing.isnbells(arg)):
                raise CREError('Invalid number of bells "%s"' %arg)

        # bell
        elif vtype in ['bell']:
            if not(ringing.isbellsymbol(arg)):
                raise CREError('Invalid bell symbol "%s"' %arg)

        # callchange
        elif vtype in ['callchange']:
            if not(ringing.iscallchange(arg)):
                raise CREError('Invalid call change "%s"' %arg)

        # colour
        elif vtype in ['colour']:
            if not(rowfmt.iscolour(arg)):
                raise CREError('Invalid colour "%s"' %arg)

        # variable
        elif vtype in ['var']:
            arg1,arg2=varsep(arg)
            if arg2 not in self.vars.keys():
                raise CREError('Invalid variable "%s"' %arg2)
            elif arg1!='' and arg1 not in self.objects.keys():
                raise CREError('Invalid object "%s"' %arg1)

        # objname
        elif vtype in ['objname']:
            if not(isobjectname(arg)):
                raise CREError('Invalid object identifier name "%s"' %arg)

        # object
        elif vtype in self.object_types+['object']:
            if arg not in self.objects.keys():
                raise CREError('Invalid %s identifier "%s"' %(vtype,arg))
            elif self.objects[arg].objtype!=vtype and vtype!='object':
                raise CREError('Object "%s" is not a %s' %(arg,vtype))

        # list
        elif vtype in self.validation_lists.keys():
            if arg not in self.validation_lists[vtype]:
                raise CREError('Invalid value "%s" (valid values are: %s)'
                                 %(arg,', '.join(self.validation_lists[vtype])))

        # invalid validation rule: shouldn't get here!
        else:
            raise CREError('Invalid validation rule')

        # return argument
        return arg


    ### readconfig - read a configuration file (2 column CSV)

    def readconfig(self,filename):

        config={}

        with open(filename,'r') as fp:
            line=next(csv.reader(fp,delimiter=',',quotechar='"'))
            for line in csv.reader(fp,delimiter=',',quotechar='"'):
                config[line[0].strip()]=line[1].strip()

        return config

    ### push - push environment onto stack

    def push(self):
        self.stack.append(self.vars)
        self.vars=self.stack[-1].copy()
        self.stack.append(self.objects)
        self.objects={}
        for x in self.stack[-1].keys():
            self.objects[x]=self.stack[-1][x].copy()

    ### pop - pop environment off stack

    def pop(self):
        self.objects=self.stack.pop()
        self.vars=self.stack.pop()

    ### clearstack - clear stack

    def clearstack(self):
        if len(self.stack)>0:
            self.objects=self.stack[1]
            self.vars=self.stack[0]
            self.stack=[]

    ### message - generate a message for information

    def message(self,msg):
        if not(self.quiet) and self.vars['verbose']=='on':
            self.write('%s' %msg)


    ### makeshortcut: make shortcut on desktop

    def makeshortcut(self,cls,pyw=False):
        filename=os.path.join(self.homedir,'Desktop',cls.info['name'])
        shebang='#!%s' %sys.executable
        if sys.platform.startswith('win'):
            filename+=('.pyw' if pyw else '.py')
            shebang='# %s' %cls.info['name']
        with open(filename,'w') as fp:
            fp.write('%s\n%s\n' %(shebang,cls.shortcut))
        os.chmod(filename,int('755',8))
        self.message('Created shortcut "%s" on desktop' %cls.info['name'])


    ### constant class variables

    # vars_default - default values
    vars_default={
        'cover': 'off'
        , 'traceformat': 'subs'
        , 'showcall': 'on'
        , 'skel': 'off'
        , 'showpn': 'off'
        , 'showcomments': 'off'
        , 'showrule': 'on'
        , 'rulebefore': 'off'
        , 'textpages': 'on'
        , 'textwidth': '80'
        , 'textheight': '40'
        , 'textsep': '5'
        , 'commentlen': '10'
        , 'landscape': 'off'
        , 'papersize': 'A4'
        , 'leftmargin': '72'
        , 'rightmargin': '72'
        , 'topmargin': '72'
        , 'bottommargin': '72'
        , 'borderwidth': '24'
        , 'commentwidth': '0'
        , 'fontsize': '12'
        , 'weightR': 'medium'
        , 'colourR': '000000'
        , 'colourP': '000080'
        , 'colourX': 'FF0000'
        , 'columnsep': '36'
        , 'nleads': '1'
        , 'imgscale': '1'
        , 'pagenumbering': 'on'
        , 'tracebells': '12'
        , 'commentoffset': '0'
        , 'repeatrow': '1'
        , 'pealtime': '150'
        , 'cartwheel': 'off'
        , 'tempo': '180'
        , 'strike': 'on'
        , 'pagedoc': 'off'
        , 'pagerows': 'off'
        , 'pager': ''
        , 'shell': ''
        , 'verbose': 'on'
        , 'ui_export_file': 'Export.html'
        , 'ui_current_mode': 'p'
        , 'ui_current_touch': ''
        , 'ui_repeat': 'off'
        , 'sound': 'none'
        , 'gspath': 'gs'
        , 'volumes': 'plain,principle,trebledodging'
        }

    # vars_win32: platform specific settings (windows)
    vars_win32={
        'traceformat': 'subs'
        , 'pager': 'more'
        , 'shell': 'C:\\Windows\\System32\\Cmd.exe'
        , 'sound': 'playsound'
        , 'gspath': 'C:\\Program Files\\gs\\gs9.50\\bin\\gswin64c.exe'
        }

    # vars_darwin: platform specific settings (macOS)
    vars_darwin={
        'traceformat': 'ansi'
        , 'pager': 'less'
        , 'shell': '/bin/sh'
        , 'sound': 'nssound'
        , 'gspath': 'gs'
        }

    # vars_linux: platform specific settings (linux etc)
    vars_linux={
        'traceformat': 'ansi'
        , 'pager': 'less'
        , 'shell': '/bin/bash'
        , 'sound': 'pygame'
        , 'gspath': 'gs'
        }

    # default colour and weights sequences for tracing
    colours_default=['red','blue','magenta','green','yellow','cyan','grey','black']
    weights_default=['medium']

    # validation_var: variable validations
    validation_var={
        'showcall': 'boolean'
        , 'cover': 'boolean'
        , 'skel': 'boolean'
        , 'showpn': 'boolean'
        , 'showrule': 'boolean'
        , 'rulebefore': 'boolean'
        , 'landscape':'boolean'
        , 'strike': 'boolean'
        , 'nleads': 'number'
        , 'imgscale': 'number'
        , 'textpages': 'boolean'
        , 'textwidth': 'number'
        , 'textheight': 'number'
        , 'commentlen': 'number'
        , 'textsep': 'number'
        , 'leftmargin': 'number'
        , 'rightmargin': 'number'
        , 'topmargin': 'number'
        , 'bottommargin': 'number'
        , 'borderwidth': 'number'
        , 'commentwidth': 'number'
        , 'fontsize': 'number'
        , 'columnsep': 'number'
        , 'papersize': 'papersize'
        , 'traceformat': 'traceformat'
        , 'pagenumbering': 'boolean'
        , 'commentoffset': 'number'
        , 'colour*': 'colour'
        , 'weight*': 'weight'
        , 'repeatrow': 'number'
        , 'tempo': 'decimal'
        , 'pealtime': 'number'
        , 'cartwheel': 'boolean'
        , 'pagedoc': 'boolean'
        , 'pagerows': 'boolean'
        , 'verbose': 'boolean'
        , 'ui_current_mode': 'mode'
        , 'ui_repeat': 'boolean'
        , 'sound': 'sound'
        }

    # object_types: Object types
    object_types=['block','method','tower']

    # validation_lists: Validation lists
    validation_lists={
        'boolean': ['off','on']
        , 'papersize': ['A3','A4','A5','B5','letter','legal']
        , 'traceformat': ['plain','subs','overstrike','ansi']
        , 'weight': ['fine','medium','bold']
        , 'mode': ['p','t']
        , 'sound': ['none','nssound','pygame','playsound','winsound']
        }

    # info: program info
    info={
        'name': 'Change Ringing Engine'
        , 'fullname': 'Change Ringing Engine'
        , 'author': 'Jonathan Wilson'
        , 'url': 'www.harrogatebellringers.org/bellview'
        , 'year': '2020'
        , 'version': '3.1.1'
        , 'release': '26 May 2020'
        }

    # shortcut: content for shortcut script
    shortcut='''\
from sys import argv, exit
from crengine import Engine
r=Engine().runengine(argv[1:])
exit(r)
'''

    # non_warranty: non-warranty message
    non_warranty='''\
This program comes with ABSOLUTELY NO WARRANTY. This is free software,
and you are welcome to redistribute it under certain conditions; type
"help licence" for details.'''

    # help_usage: usage banner for -h
    help_usage='''\
USAGE

    python -m crengine [OPTION] ... [OPTION] [FILE] ... [FILE]

OPTIONS

    -b          Batch mode - do not enter interactive session
    -d          Force rebuilding of the method library
    -h          Display this message and exit
    -l          Display the licence and exit
    -i          Bypass initialisation file
    -v          Display version information and exit
    -z          Create desktop icon and exit

    -e COMMAND  Run a CRE command
    -f FILE     Input a file into the CRE session
    -m VOLUMES  Select method volumes
    -o FILE     Redirect output to file
    -r FILE     Restore a session
    -s VAR=VAL  Set a CRE variable
    -t MODULE   Select sound module
'''







######################################################################
### Global functions
######################################################################

### indent

def indent(n,txt):
    return '\n'.join([(n*' ')+t for t in txt.split('\n')])


### isnumber - return true if string is a number and is in range

def isnumber(s,nmin=None,nmax=None):
    r=s.isdigit() or (s[0] in ['-','+'] and s[1:].isdigit())
    if r and nmin is not None:
        r=int(s)>=nmin
    if r and nmax is not None:
        r=int(s)<=nmax
    return r


### isdecimal

def isdecimal(s):
    s1,d,s2=s.partition('.')
    return (len(s1)>0 or len(s2)>0) and ('0'+s1).isdigit() and (s2+'0').isdigit()

### varsep - separate block.variable

def varsep(s):
    s1,d,s2=s.partition('.')
    return (s1,s2) if d=='.' else ('',s1)

### isobjectname - checks a string for validity as an object name

def isobjectname(s):
    return s.replace('_','').isalnum() and s[0:1].isalpha() and len(s)>0 and len(s)<64







