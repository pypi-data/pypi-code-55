######################################################################
### Change Ringing Engine
### Copyright (c) 2020 Jonathan Wilson
### Please refer to help/licence.txt for further information
### File: rowset.py
### Description: Typesetting of rows
### Last Modified: 24 May 2020
######################################################################

### import modules

from time import sleep
from . import ringing


######################################################################
### Format
######################################################################

class Format():

    ### initialisation

    def __init__(self,nbells,leadlen,canvas,singlepage,singlecolumn):

        # parameters
        self.nbells=nbells             # number of bells
        self.leadlen=leadlen           # length of lead
        self.canvas=canvas             # canvas/text mode
        self.singlecolumn=singlecolumn # single column
        self.singlepage=singlepage     # single page

        # disable singlepage if in text mode
        if not(self.canvas) and self.singlepage:
            self.singlepage=False

        # disable singlecolumn if in canvas mode
        if self.canvas and self.singlecolumn:
            self.singlecolumn=False

        # geometry
        self.nleads=1                  # leads per column
        self.nrows=self.leadlen        # rows per column
        self.ncols=4                   # columns per page
        self.rowwidth=self.nbells      # row width (chars)

        # formatting options
        self.skel=False                # skeleton format  
        self.showcall=True             # show calls
        self.showpn=True               # show place notation
        self.showcomments=True         # show comments
        self.showrule=True             # show rules 
        self.rulebefore=False          # rule before lead ends
        self.commentlen=0              # comment length

        # text mode defaults
        self.textwidth=80              # width of page (chars)
        self.textheight=40             # height of page (chars)
        self.textsep=5                 # column separation (chars)

        # canvas mode defaults
        self.papersize='A4'            # paper size
        self.landscape=False           # landscape
        self.pagewidth=595             # width of page (pt)
        self.pageheight=842            # height of page (pt)
        self.leftmargin=72             # left margin (pt)
        self.rightmargin=72            # right margin (pt)
        self.topmargin=72              # top margin (pt)
        self.bottommargin=72           # bottom margin (pt)
        self.borderwidth=24            # single page border width (pt)
        self.columnsep=36              # column separation (pt)    
        self.fontsize=12               # font size (pt)

        # fonts and colours
        self.rulecolour='000000'       # rule colour
        self.rulethickness=2           # rule thickness
        self.pncolour='000080'         # place notation colour
        self.commentcolour='FF0000'    # comment colour

        # separation between lines (pt)
        self.baselinesep=int(self.fontsize*1.2)

        # nominal width of a single character (pt)
        self.charsep=int(self.fontsize*0.85)

        # width of a column (pt)
        self.columnwidth=self.charsep*self.rowwidth

        # row space
        self.rowspace=' '*self.textsep

        # rule string
        self.rulestr='-'*self.nbells

        # bell symbols
        self.bellsyms=[' ']+list(map(
                ringing.bellsymbol,range(1,self.nbells+1)))

        # trace colours
        self.tracecolours={}

        # trace weights
        self.traceweights={}


    ### str

    def __str__(self):

        items=[
            ('nbells',self.nbells)
            , ('leadlen',self.leadlen)
            , ('nleads',self.nleads)
            , ('nrows',self.nrows)
            , ('ncols',self.ncols)
            , ('rowwidth',self.rowwidth)
            , ('bellsyms',''.join(self.bellsyms[1:]))
            , ('pagewidth',self.pagewidth)
            , ('pageheight',self.pageheight)
            ]

        return '\n'.join(['%-10s%s' %(a,b) for a,b in items])


    ### set - set up format

    def set(self,vars):

        # get formatting parameters
        self.nleads=getnum(vars,'nleads',self.nleads)
        self.skel=getbool(vars,'skel',self.skel)
        self.showcall=getbool(vars,'showcall',self.showcall)
        self.showpn=getbool(vars,'showpn',self.showpn)
        self.showcomments=getbool(vars,'showcomments',self.showcomments)
        self.showrule=getbool(vars,'showrule',self.showrule)
        self.rulebefore=getbool(vars,'rulebefore',self.rulebefore)
        self.commentlen=getnum(vars,'commentlen',self.commentlen)

        # calculate rowwidth
        self.rowwidth=self.nbells
        if self.showcall:
            self.rowwidth+=2
        if self.showpn:
            self.rowwidth+=self.nbells-1
        if self.showcomments:
            self.rowwidth+=self.commentlen+1

        # get text mode parameters
        self.textwidth=getnum(vars,'textwidth',self.textwidth)
        self.textheight=getnum(vars,'textheight',self.textheight)
        self.textsep=getnum(vars,'textsep',self.textsep)
        self.rowspace=' '*self.textsep

        # get canvas mode parameters
        self.papersize=vars.get('papersize',self.papersize).upper()
        self.landscape=False # TBD
        self.leftmargin=getnum(vars,'leftmargin',self.leftmargin)
        self.rightmargin=getnum(vars,'rightmargin',self.rightmargin)
        self.topmargin=getnum(vars,'topmargin',self.topmargin)
        self.bottommargin=getnum(vars,'bottommargin',self.bottommargin)
        self.borderwidth=getnum(vars,'borderwidth',self.borderwidth)
        self.columnsep=getnum(vars,'columnsep',self.columnsep)
        self.fontsize=getnum(vars,'fontsize',self.fontsize)
        self.baselinesep=int(self.fontsize*1.2)
        self.charsep=int(self.fontsize*0.85)
        self.columnwidth=self.charsep*self.rowwidth

        # fonts and colours
        self.rulecolour=getcolour(vars,'R','black')
        self.pncolour=getcolour(vars,'P','black')
        self.commentcolour=getcolour(vars,'X','black')
        self.rulethickness=getweight(vars,'R','medium',self.fontsize)

        # page width / height - based on paper size

        paperdims={
            'A3': (842,1190)
            , 'A4': (595,842)
            , 'A5': (420,595)
            , 'B5': (499,709)
            , 'letter': (612,792)
            , 'legal': (612,1008)
            }

        self.pagewidth,self.pageheight=paperdims[self.papersize]


        # adjust geometry

        if self.canvas and self.singlepage:

            ## single page canvas (SVG, EPS etc)

            self.leftmargin=self.borderwidth
            self.rightmargin=self.borderwidth
            self.topmargin=self.borderwidth
            self.bottommargin=self.borderwidth
            self.nrows=self.nleads*self.leadlen
            self.ncols=10 # arbitrary
            self.pagewidth=self.ncols*self.columnwidth
            self.pagewidth+=(self.ncols-1)*self.columnsep
            self.pagewidth+=self.leftmargin+self.rightmargin
            self.pageheight=(self.nrows+1)*self.baselinesep
            self.pageheight+=self.topmargin+self.bottommargin

        elif self.canvas:

            ## multiple page canvas (PS, PDF)

            # number of leads
            self.nleads=(
                self.pageheight-self.topmargin-self.bottommargin-self.baselinesep)//(
                self.leadlen*self.baselinesep)
            if self.nleads<1:
                self.nleads=1

            # number of rows
            self.nrows=self.nleads*self.leadlen

            # number of columns
            self.ncols=int(
                self.pagewidth+self.columnsep-self.leftmargin-self.rightmargin)//int(
                self.columnwidth+self.columnsep)
            if self.ncols<1:
                self.ncols=1

        else:

            ## text mode

            # calculate nleads
            self.nleads=(self.textheight-1)//(self.leadlen+int(self.showrule))
            if self.nleads<1:
                self.nleads=1

            # number of rows
            self.nrows=self.nleads*self.leadlen

            # calculate ncols
            self.ncols=(self.textwidth+self.textsep)//(self.rowwidth+self.textsep)
            if self.ncols<1:
                self.ncols=1


    ### trace

    def trace(self,traceformat,vars):

        # clear trace bells
        self.tracecolours.clear()
        self.traceweights.clear()
        tracebells=vars['tracebells'].upper()

        ## set up traces

        for b in tracebells:
            n=ringing.bellnumber(b)
            if 1<=n<=self.nbells and 'colour'+b in vars.keys():
                self.tracecolours[n]=hexcolour(vars.get('colour'+b,'black'))
                self.traceweights[n]=linethickness(vars.get('weight'+b,'medium'),self.fontsize)

        # skeleton format - replace non-trace bells by a '.'
        if self.skel:
            for i in range(1,self.nbells+1):
                if i not in self.tracecolours.keys():
                    self.bellsyms[i]='.'

        ## apply trace to bell symbols for text modes

        # substitution
        if traceformat in ['subs']:
            for k in self.tracecolours.keys():
                self.bellsyms[k]='*'

        # overstrike
        elif traceformat in ['over']:
            for k in self.tracecolours.keys():
                self.bellsyms[k]=self.bellsyms[k]+'\010'+self.bellsyms[k]

        # ANSI
        elif traceformat in ['ansi']:
            for k in self.tracecolours.keys():
                self.bellsyms[k]=ansicolour(self.tracecolours[k],self.bellsyms[k])

        # plain
        else:
            pass


    ### blockstrike - silently ring block

    def blockstrike(self,block):
        for row in block.rows:
            self.rowstrike(row)

    ### rowstrike - silently ring row

    def rowstrike(self,row):
        print(self.typesetrow(row))
        sleep(2)

    ### typesetrow

    def typesetrow(self,row):

        txt=''

        # call symbol
        if self.showcall:
            txt+='%-2s' %row.call

        # bells
        txt+=row.format(self.bellsyms,'',self.nbells)

        # place notation
        if self.showpn:
            txt+=' %-*.*s' %(self.nbells-2,self.nbells-2,row.pn)

        # comments
        if self.showcomments:
            txt+=' %-*.*s' %(self.commentlen,self.commentlen,row.comment)

        return txt


######################################################################
### Global Functions
######################################################################


### colour names

colournames={
'black':'000000'
,'darkred':'800000'
,'darkgreen':'008000'
,'darkyellow':'808000'
,'darkblue':'000080'
,'darkmagenta':'800080'
,'darkcyan':'008080'
,'grey':'808080'
,'lightgrey':'C0C0C0'
,'red':'FF0000'
,'green':'00FF00'
,'yellow':'FFFF00'
,'blue':'0000FF'
,'magenta':'FF00FF'
,'cyan':'00FFFF'
,'white':'FFFFFF'
}

### ANSI colour set

ansi_colours={
    '000000': '\033[30m'
    , '800000': '\033[31m'
    , '008000': '\033[32m'
    , '808000': '\033[33m'
    , '000080': '\033[34m'
    , '800080': '\033[35m'
    , '008080': '\033[36m'
    , 'C0C0C0': '\033[37m'
    , '808080': '\033[90m'
    , 'FF0000': '\033[91m'
    , '00FF00': '\033[92m'
    , 'FFFF00': '\033[93m'
    , '0000FF': '\033[94m'
    , 'FF00FF': '\033[95m'
    , '00FFFF': '\033[96m'
    , 'FFFFFF': '\033[97m'
    }

### ansi_off - turn ANSI colour off

ansi_off='\033[0m'

### ansicolour - display text using nearest ANSI colour

def ansicolour(s,txt):
    (r1,g1,b1)=rgbcolour(s)
    if r1<0:
        return txt

    d1=3*255**2
    d2=d1
    c=''

    for t in ansi_colours.keys():
        
        (r2,g2,b2)=rgbcolour(t)
        d2=(r2-r1)**2+(g2-g1)**2+(b2-b1)**2

        if d2<d1:
            c=ansi_colours[t]
            d1=d2

    return '%s%s%s' %(c,txt,ansi_off)


### rgbcolour - hex colour to (r,g,b) triple

def rgbcolour(s):
    t=hexcolour(s)
    r=int(t[0:2],16)
    g=int(t[2:4],16)
    b=int(t[4:6],16)
    return (r,g,b)


### iscolour - check a string is a valid colour (hex or name)

def iscolour(s):
    t=hexcolour(s)
    return len(t)==6 and all(
        c in '0123456789ABCDEF' for c in t)


### hexcolour - convert colour name to hex

def hexcolour(s):
    return colournames.get(s.lower(),s.upper())


### linethickness - convert weight into line thickness by fontsize

def linethickness(weight,fontsize):
    weights={'fine':0.1,'medium':0.2,'bold':0.3}
    return int(fontsize*weights.get(weight,0.2))


### getnum - get numeric value from dictionary

def getnum(vars,key,default):
    if key in vars.keys():
        val=int(vars[key])
    else:
        val=default
    return val


### getbool - get boolean value from dictionary

def getbool(vars,key,default):
    if key in vars.keys():
        val=(vars[key]=='on')
    else:
        val=default
    return val


### getcolour - get colour value from dictionary

def getcolour(vars,key,default):
    return hexcolour(vars.get('colour'+key,default))


### getthickness - get thickness value from dictionary

def getweight(vars,key,default,fontsize):
    return linethickness(vars.get('weight'+key,default),fontsize)


