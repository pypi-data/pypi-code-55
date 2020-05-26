######################################################################
### Change Ringing Engine
### Copyright (c) 2020 Jonathan Wilson
### Please refer to help/licence.txt for further information
### File: ringing.py
### Description: Defines change-ringing classes Method, Block, Change
### Last Modified: 24 May 2020
######################################################################

### import modules

import re

######################################################################
### Class: RingObj - generic CRE object
######################################################################

class RingObj():

    ### Initialise object

    def __init__(self,objtype,name,nbells):
        self.objtype=objtype
        self.name=name
        self.nbells=nbells
        self.stagename=getstagename(nbells)
        self.vars={}

    ### str() - return name

    def __str__(self):
        return '"%s"' %self.name

    ### copy - copy object

    def copy(self):
        obj=RingObj(self.objtype,self.name,self.nbells)
        obj.xfer(self)
        return obj

    ### xfer - transfer attributes from another object

    def xfer(self,obj):
        self.vars=obj.vars.copy()

    ### show - show object (may override)

    def show(self):
        return self.showattribs()+'\n'+self.showvars()

    ### showattribs - show attributes

    def showattribs(self):

        s='''Attributes:
Name            : %s
Type            : %s
Number of Bells : %d
''' % (self.name,self.objtype.title(),self.nbells)

        return s

    ### showvars - show variables

    def showvars(self):
        vs='\n'.join(
            ['%s = %s' % (n,self.vars[n])
             for n in sorted(self.vars.keys())])

        s='Variables:\n%s\n' %vs
        return s




######################################################################
### Class: Method
######################################################################

class Method(RingObj):

    ### Initialise method

    def __init__(self,basename,nbells):

        # form full name
        name=basename+' '+getstagename(nbells).title()

        # initialise parent object
        RingObj.__init__(self,'method',name,nbells)

        # method parameters
        self.basename=basename
        self.pn=''
        self.offset=0
        self.leadlen=0
        self.nleads=0
        self.plainleads=[]

        # call parameters
        self.callpos=0
        self.bobpn=''
        self.singlepn=''
        self.bobs=None
        self.singles=None


    ### Recall method as string

    def __str__(self):
        fields=[self.basename,self.nbells,self.pn,self.callpos,self.bobpn,self.singlepn]
        return ' '.join(['"%s"' %f for f in fields])

    ### copy method

    def copy(self):

        mtd=Method(self.basename,self.nbells)
        mtd.xfer(self)
        mtd.pn=self.pn
        mtd.offset=self.offset
        mtd.leadlen=self.leadlen
        mtd.nleads=self.nleads
        mtd.callpos=self.callpos
        mtd.bobpn=self.bobpn
        mtd.singlepn=self.singlepn

        for ld in self.plainleads:
            mtd.plainleads.append(ld.copy())

        if self.bobs is not None:
            mtd.bobs=[]
            for ld in self.bobs:
                mtd.bobs.append(ld.copy())

        if self.singles is not None:
            mtd.singles=[]
            for ld in self.singles:
                mtd.singles.append(ld.copy())

        return mtd


    ### show - show definition of method

    def show(self):

        block=Block('temp',self.nbells)
        self.ringplainlead(block)

        s='''\
Place Notation  : %s
Calling Row     : %d
Bob             : %s
Single          : %s

Plain Lead:
''' %(self.pn, self.callpos, self.bobpn, self.singlepn)

        return self.showattribs()+s+block.dump()+'\n\n'+self.showvars()


    ### setmethod - set up method

    def setmethod(self,pn):

        # place notation (remove spaces and uppercase)
        self.pn=pn.replace(' ','').upper()

        # extract offset
        self.offset=0
        pn2,sep,offset=self.pn.partition('<')
        if offset.isdigit():
            self.offset=int(offset)

        # split plainleads of multiple plain-lead methods
        # e.g. Stedman quick and slow sixes
        pns=pn2.split('|')

        # number of plain leads
        self.nleads=len(pns)

        # define plain lead(s)
        self.plainleads=[]
        for p in pns:
            plainlead=Block('%s: Plain Lead' %self.name,self.nbells)
            plainlead.appendpncomp(p)
            plainlead.rows[-1].leadend=True
            self.plainleads.append(plainlead)

        # lead length
        self.leadlen=self.plainleads[0].len

        # normalise offset
        self.offset=self.offset%self.leadlen

        # clear bobs/singles
        self.callpos=0
        self.bobpn=''
        self.singlepn=''
        self.bobs=None
        self.singles=None

    ### Dump - dump a method

    def dump(self):

        print('Method: %s' %self.name)
        print('\nBells: %d' %self.nbells)

        print('\nPlain Leads: %s' %self.pn)
        for i,plainlead in enumerate(self.plainleads):
            print('Plain Lead %d' %i)
            plainlead.dump()

        print('\nLead length      %d' %self.leadlen)
        print('Offset           %d' %self.offset)
        print('Calling Position %d' %self.callpos)

        print('\nBob: %s' %self.bobpn)
        if self.bobs is None:
            print('None')
        else:
            for i,bob in enumerate(self.bobs):
                print('Bob %d' %i)
                bob.dump()

        print('\nSingle: %s' %self.singlepn)
        if self.singles is None:
            print('None')
        else:
            for i,single in enumerate(self.singles):
                print('Single %d' %i)
                single.dump()


    ### Add calls

    def setcalls(self,callpos,bobpn,singlepn):

        # get calling position
        self.callpos=callpos%self.leadlen
        if self.callpos==0:
            self.callpos=self.leadlen

        # lead end row in call
        ldendrow=self.leadlen-self.callpos+1

        # bob place notation(s) - strip and uppercase
        self.bobpn=bobpn.replace(' ','').upper()

        # bob(s)
        self.bobs=None
        if len(self.bobpn)>0:
            self.bobs=[]
            for p in self.bobpn.split('|'):
                bob=Block('%s: Bob' %self.name,self.nbells)
                bob.appendpn(p)
                if 1<=ldendrow<=bob.len:
                    bob.rows[ldendrow].leadend=True
                self.bobs.append(bob)
            l=len(self.bobs)
            for i in range(l,self.nleads):
                self.bobs.append(bob)

        # single place notation(s) - strip and uppercase
        self.singlepn=singlepn.replace(' ','').upper()

        # single(s)
        self.singles=None
        if len(self.singlepn)>0:
            self.singles=[]
            for p in self.singlepn.split('|'):
                single=Block('%s: Single' %self.name,self.nbells)
                single.appendpn(p)
                if 1<=ldendrow<=single.len:
                    single.rows[ldendrow].leadend=True
                self.singles.append(single)
            l=len(self.singles)
            for i in range(l,self.nleads):
                self.singles.append(single)


    ### ringplainlead - ring a plain lead

    def ringplainlead(self,block):

        # unmark previous row as leadend if offset is non-zero
        if self.offset!=0:
            block.rows[-1].leadend=False

        # allow first lead to start at row determined by offset
        # this allows Stedman to be correctly rung
        for row in self.plainleads[0].rows[1+self.offset:]:
            block.ring(row)

        # ring remaining leads
        for plainlead in self.plainleads[1:]:
            for row in plainlead.rows[1:]:
                block.ring(row)

        # add missing rows from the first lead
        for row in self.plainleads[0].rows[1:1+self.offset]:
            block.ring(row)


    ### ringplaincourse - ring a plain course

    def ringplaincourse(self,block):
        initial=block.lastrow()
        self.ringplainlead(block)
        while not initial.eq(block.lastrow()):
            self.ringplainlead(block)


    ### ringtouch - ring a touch

    def ringtouch(self,block,calls):

        # extract P,B,S
        leadtypes=''.join([a for a in calls.upper() if a in 'PBS'])

        # for multiple lead methods (e.g. Stedman), force the number of leads
        # in the touch to be a multiple of the number of leads/divisions
        # of the method i.e. can't ring a quick six without a slow six!

        if self.nleads>1 and len(leadtypes)%self.nleads>0:
            leadtypes+='P'*(self.nleads-len(leadtypes)%self.nleads)

        # add a plain dummy lead if offset>0
        if self.offset>0:
            if self.callpos>self.offset:
                leadtypes+='P'
            else:
                leadtypes='P'+leadtypes

        # current work
        work='P'

        # row counter for inside calls
        s=1

        # call indicator
        call=''


        for k in range(0,len(leadtypes)):

            # which lead to ring: usually "0" unless
            # multiple lead method e.g. Stedman
            ld=k%self.nleads

            # lead type (bob/single/plain)
            lt=leadtypes[k]

            # first row - normally 1 unless 1st lead with offset>0
            firstrow=1
            if k==0 and self.offset>0:
                firstrow=1+self.offset

            # lastrow - normally leadlen unless last lead with offset>0
            lastrow=self.leadlen
            if k==len(leadtypes)-1 and self.offset>0:
                lastrow=self.offset


            for r in range(firstrow,lastrow+1):

                # If calling position is reached and the lead is a bob
                # then enter the working of the bob

                if (r-self.callpos)%self.leadlen==0 and lt=='B' and self.bobs is not None:
                    work='B'
                    call='-'
                    s=1

                # If calling position is reached and the lead is a single
                # then enter the working of the single

                if (r-self.callpos)%self.leadlen==0 and lt=='S' and self.singles is not None:
                    work='S'
                    call='S'
                    s=1

                # Get the next transposition, either from the plain lead
                # or the bob or single. If the bob or single end has been
                # reached then revert back to the plain lead

                if work=='B':
                    transp=self.bobs[ld].rows[s]
                    s+=1
                    
                    if s>self.bobs[ld].len:
                        work='P'

                elif work=='S':
                    transp=self.singles[ld].rows[s]
                    s+=1

                    if s>self.singles[ld].len:
                        work='P'

                else:

                    transp=self.plainleads[ld].rows[r]

                # ring the next change and reset call indicator
                # immediately so that it persists on the first
                # row of the call only

                block.ring(transp)
                block.rows[-1].call=call
                call=''


######################################################################
### Class: Block
######################################################################

class Block(RingObj):

    ### initialisation

    def __init__(self,name,nbells):

        # initialise parent
        RingObj.__init__(self,'block',name,nbells)

        # initialise other parameters
        self.leadlen=0
        self.len=0
        self.rang=0
        self.rows=[]
        self.rows.append(Change(nbells))
        self.rows[-1].leadend=True

    ### str

    def __str__(self):
        fields=[self.name,self.nbells,self.leadlen]
        return ' '.join(['"%s"' %f for f in fields])

    ### copy

    def copy(self):
        blk=Block(self.name,self.nbells)
        blk.xfer(self)
        blk.leadlen=self.leadlen
        blk.len=self.len
        blk.rang=self.rang
        blk.rows=[]
        for r in self.rows:
            blk.rows.append(r)
        return blk

    ### show

    def show(self):

        s='''\
Lead Length     : %s
Number of Rows  : %s
''' % (self.leadlen, self.len)

        return self.showattribs()+s+'\n'+self.showvars()

    ### Dump

    def dump(self):
        return '\n'.join([
                '%5d %s' %(r,self.rows[r])
                for r in range(0,self.len+1)])

    ### clear - remove all rows

    def clear(self):
        self.len=0
        self.rang=0
        self.rows=[]
        self.rows.append(Change(self.nbells))
        self.rows[-1].leadend=True


    ### plainhunt - ring plain hunt

    def ringplainhunt(self,nbells):

        # place notation generator
        b=bellsymbol(nbells)
        p='.X.1'+b if nbells%2==0 else '.'+b+'.1'

        # place notation for lead
        pn=(p*nbells)[1:]

        # define lead
        lead=Block('temp',nbells)
        lead.appendpncomp(pn)

        # ring the lead
        self.ringlead(lead)


    ### repeat - repeat existing rows as changes until it comes round

    # TBD - add some form of checking to prevent endless loop

    def repeat(self):
        changes=self.rows[1:]
        while not(self.cameround()):
            leadhead=self.lastrow()
            for change in changes:
                newrow=leadhead.copy()
                newrow.permutate(change)
                self.append(newrow)

    ### ringlead - ring a lead (from a block of transpositions)

    def ringlead(self,lead):
        for row in lead.rows[1:]:
            self.ring(row)


    ### appendpncomp - append compound place notation

    def appendpncomp(self,pn):
        for p in pn.split(','):
            self.appendpn(p)


    ### appendpn - derive next changes by place notation

    def appendpn(self,pn):

        # determine if the place notation is palindromic
        palindromic=False
        if pn[0]=='&':
            palindromic=True
            pn=pn[1:]

        # force uppercase
        pn=pn.upper()

        # insert separators around cross-overs
        pn=re.sub('[X\-]','.X.',pn)

        # remove leading, trailing and duplicate separators
        pn=re.sub('\.+','.',pn)
        pn=re.sub('^\.','',pn)
        pn=re.sub('\.$','',pn)

        # split place notation string into rows
        ps=pn.split('.')

        # separate half lead
        hl=ps.pop()

        # reverse place notation
        pr=ps[:]
        pr.reverse()

        # working change
        ch=Change(self.nbells)

        # ring forward place notation
        for p in ps:
            ch.setpn(p)
            self.append(ch)

        # Ring half-lead
        ch.setpn(hl)
        self.append(ch)

        # Ring reverse place notation
        if palindromic:
            for p in pr:
                ch.setpn(p)
                self.append(ch)


    ### ring - derive next change from previous

    def ring(self,ch):
        ch2=self.rows[-1].copy()
        ch2.permutate(ch)
        self.rows.append(ch2)
        self.len+=1
        self.rang+=1

    ### append - append a new change

    def append(self,ch):
        ch2=ch.copy()
        self.rows.append(ch2)
        self.len+=1
        self.rang+=1

    ### callchange - ring a call change "a" to "b"

    def callchange(self,a,b):
        ch=self.rows[-1].copy()
        ch.callchange(a,b)
        self.rows.append(ch)
        self.len+=1
        self.rang+=1
        self.rows[-1].leadend=(self.len%self.leadlen==0)
    
    ### cameround - check that last change is same as initial change

    def cameround(self):
        return self.lastrow().eq(self.initrow())

    ### initrow -return initial (reference) row

    def initrow(self):
        return self.rows[0]

    ### lastrow - return last row

    def lastrow(self):
        return self.rows[-1]

    ### addcomment - add a comment to a row

    def addcomment(self,rowno,comment):
        self.rows[rowno].comment=comment

    ### delcomment - delete a comment from a row

    def delcomment(self,rowno):
        self.rows[rowno].comment=''

    ### showcomments - return a list of comments

    def showcomments(self):
        content=[]
        for rowno in range(0,self.len+1):
            if self.rows[rowno].comment!='':
                content.append('%d "%s"' %(rowno,self.rows[rowno].comment))
        return '\n'.join(content)


######################################################################
### Class: Change
######################################################################

class Change():

    ### Initialisation

    def __init__(self,nbells):
        self.nbells=nbells
        self.call=''
        self.places=list(range(0,nbells+1))
        self.pn=''
        self.leadend=False
        self.comment=''

    def __str__(self):
        return '%1s %s%1s %s' %(
            self.call
            ,self.get()
            ,'*' if self.leadend else ''
            ,self.pn)

    ### copy - copy the entire object

    def copy(self):
        ch=Change(self.nbells)
        ch.call=self.call
        ch.places=self.places[:]
        ch.pn=self.pn
        ch.leadend=self.leadend
        ch.comment=self.comment
        return ch

    ### Dump

    def dump(self):
        print(str(self))

    ### format - output as formatted row

    def format(self,bellsyms,delim,nbells):
        return delim.join(
            [bellsyms[p] for p in self.places[1:]]
            +[bellsyms[n] for n in range(self.nbells+1,nbells+1)])

    ### setrounds - set to rounds

    def setrounds(self):
        self.places=list(range(0,self.nbells+1))
        self.pn=''

    ### set - set to row in symbolic bell notation

    def set(self,bells):
        self.places=[0]+[bellnumber(b) for b in bells]
        self.pn=''

    ### get - return change as row in symbolic bell notation

    def get(self):
        return ''.join([bellsymbol(x) for x in self.places[1:]])

    ### setpn - set change as transposition by place notation

    def setpn(self,pn):
        self.setrounds()
        self.applypn(pn)

    ### applypn - transpose according to place notation

    def applypn(self,pn):
        tr=[]
        q=-1
        for p in range(1,self.nbells):
            if pn.find(bellsymbol(p))<0 and pn.find(bellsymbol(p+1))<0 and p-1!=q:
                tr.append(p)
                q=p
        self.transpose(tr)
        self.pn=pn

    ### transpose

    def transpose(self,ts):
        for t in ts:
            self.places[t+1],self.places[t]=self.places[t],self.places[t+1]

    ### permutate

    def permutate(self,ch):
        self.call=ch.call
        self.places=[0]+[self.places[p] for p in ch.places[1:]]
        self.places+=list(range(ch.nbells+1,self.nbells+1))
        self.pn=ch.pn
        self.leadend=ch.leadend

    ### isvalid - determine whether a change is valid

    def isvalid(self):

        f=True
        for i in range(1,self.nbells+1):
            f=f and (i in self.places)

        return f


    ### test for rounds

    def isrounds(self):
        f=True
        for x,y in zip(self.places[1:],range(1,self.nbells+1)):
            f=f and x==y
        return f

    ### test for change equality

    def eq(self,ch):
        f=True
        for x,y in zip(self.places[1:],ch.places[1:]):
            f=f and x==y
        return f


    ### parity - determine whether change is odd (False) or even (True)

    # Parity is whether an odd or even number of transpositions is required
    # to take it back to rounds. It is determined by bubble sorting the
    # places in the change!

    def parity(self):

        ch=self.copy()
        f=True

        for i in range(1,self.nbells+1):
            for j in range(i+1,self.nbells+1):
                if ch.places[j]<ch.places[i]:
                    ch.places[i],ch.places[j]=ch.places[j],ch.places[i]
                    f=not(f)

        return f


    ### order - minimum number of times to come round

    def order(self):

        ch=self.copy()
        n=1

        while not(ch.isrounds()):
            ch.permutate(self)
            n+=1

        return n

    ### callchange - swap around a pair of bells, referred to by numbers
    ### "a" to "b" moves bell "a" to follow fixed place bell "b"
    ### It works for both calling down and calling up

    def callchange(self,b1,b2):

        # get bell numbers
        n1=bellnumber(b1)
        n2=bellnumber(b2)

        # do nothing if bell numbers are out of range
        # TBD - should generate an error?
        if n1>self.nbells or n2>self.nbells:
            return

        # find bell numbers in row
        i=self.places.index(n1)
        j=self.places.index(n2)

        if i>j+1:
            # call down
            self.places=self.places[0:j+1]+self.places[i:i+1]+self.places[j+1:i]+self.places[i+1:]

        elif i<j and i>0:
            # call up
            self.places=self.places[0:i]+self.places[i+1:j+1]+self.places[i:i+1]+self.places[j+1:]

        else:
            pass


######################################################################
### Global Functions
######################################################################

# Limits on nbells

nbells_min=3
nbells_max=22

# Bell symbols

bell_symbols='1234567890ETABCDFGHJKL'

# Stage names - names associated with particular numbers of bells

stagenames={
    3:'singles'
    , 4: 'minimus'
    , 5: 'doubles'
    , 6: 'minor'
    , 7: 'triples'
    , 8: 'major'
    , 9: 'caters'
    , 10: 'royal'
    , 11: 'cinques'
    , 12: 'maximus'
    , 13: 'sextuples'
    , 14: 'fourteen'
    , 15: 'septuples'
    , 16: 'sixteen'
    , 17: 'octuples'
    , 18: 'eighteen'
    , 19: 'nineteen'
    , 20: 'twenty'
    , 21: 'twentyone'
    , 22: 'twentytwo'
    }


# Plain hunt place notation

def plainhuntpn(n):

    b=bellsymbol(n)

    if n%2:
        pn='&'+((b+'.1.')*int((n-1)/2))+b+',1'
    else:
        pn='&'+(('x1'+b)*int(n/2))+',1'

    return pn

# Valid callchange

def iscallchange(s):
    if len(s)==3:
        return isbellsymbol(s[0]) and s[1]=='-' and (isbellsymbol(s[2]) or s[2]=='.')
    elif len(s)==2:
        return isbellsymbol(s[0]) and s[1]=='-'
    else:
        return False


# Valid bell number (check upper bound only)

def isbellnumber(n):
    return n.isdigit() and 1<=int(n)<=nbells_max

# Valid bell symbol

def isbellsymbol(b):
    return b.upper() in bell_symbols

# Valid nbells

def isnbells(n):
    return n.isdigit() and nbells_min<=int(n)<=nbells_max


# Split method name into base and stage names

def splitmethodname(name):
    words=name.strip().split(' ')
    if words[-1].lower() in stagenames.values():
        nbells=getstagenbells(words[-1])
        return (' '.join(words[:-1]),words[-1],nbells)
    else:
        return (name.strip(),'',0)

# Get stage name for number of bells

def getstagename(nbells):
    return stagenames.get(nbells,'on %d bells' %nbells)

# Get number of bells from stage name

def getstagenbells(name):
    return {s:n for n,s in stagenames.items()}.get(name.lower(),0)


# Get bell number corresponding to bell symbol

def bellnumber(b):
    return ('.'+bell_symbols).find(b.upper())


# Get bell symbol corresponding to bell number

def bellsymbol(n):
    return ('.'+bell_symbols)[n]

# pad a string with spaces

def pad(s,n):
    return s.ljust(n)[:n]

# convert from string

def getboolean(s):
    return (s.lower()=='on')


# splitlines() - Extract fields from qualified space delimited line

def splitline(line):

    # Strip leading or trailing space
    line=line.strip()

    # If string is empty, return with empty list
    if line=='':
        return []

    # Split at qualifiers
    fields=line.split('"')

    # Odd fields are outside qualifiers
    # so convert whitespace to another character
    for i in range(0,len(fields),2):
        fields[i]=re.sub('[\t\ ]+','\001',fields[i])

    # Rejoin without qualifiers and split on new delimiter
    return ''.join(fields).split('\001')

