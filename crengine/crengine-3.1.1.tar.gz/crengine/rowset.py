######################################################################
### Change Ringing Engine
### Copyright (c) 2020 Jonathan Wilson
### Please refer to help/licence.txt for further information
### File: rowset.py
### Description: Typesetting of rows
### Last Modified: 24 May 2020
######################################################################

### import modules

from datetime import datetime


######################################################################
### Document: Document
######################################################################

class Document():

    ### init

    def __init__(self,fmt,title):

        self.fmt=fmt         # format
        self.title=title     # document title
        self.pagect=0        # page counter
        self.pages=[]        # list of pages

    ### str

    def __str__(self):
        txt=''
        for n,c in enumerate(self.pages):
            txt+='Page %d:\n%s' %(n+1,c)
        return txt
    
    ### addblock - add a block to the document starting on a new page

    def addblock(self,block,title):

        # begin a new column with the first row
        firstcol=Column(self.fmt,block.rows[0])

        # start a new page beginning with this column
        self.pages.append(Page(self.fmt,title))
        self.pagect+=1
        self.pages[-1].addcolumn(firstcol)

        # add rest of rows to current page
        for row in block.rows[1:]:
            self.pages[-1].addrow(row)

            # if page is overfull, remove last column to a new page
            if self.pages[-1].isfull():
                lastcol=self.pages[-1].columns.pop()
                self.pages.append(Page(self.fmt,title))
                self.pagect+=1
                self.pages[-1].addcolumn(lastcol)

        # remove orphan column
        self.pages[-1].removeorphan()

        # remove empty page
        if self.pages[-1].colct==0:
            self.pages.pop()
            self.pagect-=1

        # remove orphan rule on last column
        self.pages[-1].columns[-1].removeorphan()


    ### typeset

    def typeset(self):
        return '\f\n'.join([p.typeset() for p in self.pages])

    ### typesetcsv

    def typesetcsv(self):
        return ''.join([p.typesetcsv() for p in self.pages])




######################################################################
### Class: Page - page of multiple columns
######################################################################

class Page():

    ### init

    def __init__(self,fmt,title):

        self.fmt=fmt         # format
        self.title=title     # page title
        self.ncols=fmt.ncols # maximum number of columns
        self.colct=0         # column count
        self.columns=[]      # list of columns

    ### str

    def __str__(self):
        txt=''
        for n,c in enumerate(self.columns):
            txt+='Column %d:\n%s' %(n+1,c)
        return txt

    ### addcolumn - add a column to the page

    def addcolumn(self,column):
        self.columns.append(column)
        self.colct+=1

    ### addrow - add row to rightmost column

    def addrow(self,row):
        self.columns[-1].addrow(row)
        if self.columns[-1].isfull():
            self.columns[-1].removeorphan()
            self.addcolumn(Column(self.fmt,row))

    ### isfull - return True if page is full

    def isfull(self):
        return not(self.fmt.singlepage) and self.colct>self.ncols

    ### removeorphan - remove orphan column

    def removeorphan(self):
        if self.columns[-1].rowct==0:
            self.columns.pop()
            self.colct-=1

    ### typeset

    def typeset(self):

        txt=''

        linect=self.getlinect()

        for i in range(0,linect):
            lines=[]
            for c in self.columns:
                lines.append(c.typesetline(i))
            txt+=self.fmt.rowspace.join(lines)+'\n'

        return txt


    ### typesetcsv

    def typesetcsv(self):
        return ''.join([c.typesetcsv() for c in self.columns])


    ### getlinect - get maximum linect for page

    def getlinect(self):
        return max([0]+[c.linect for c in self.columns])




######################################################################
### Class: Column - single column of rows to be output
######################################################################

class Column():

    ### initialisation

    def __init__(self,fmt,toprow):

        self.fmt=fmt                       # format
        self.bellsyms=fmt.bellsyms         # bell symbols
        self.nbells=fmt.nbells             # number of bells
        self.showrule=fmt.showrule         # show rule
        self.rulebefore=fmt.rulebefore     # rule before leadend
        self.nrows=fmt.nrows               # number of rows (excl initial)
        self.singlecolumn=fmt.singlecolumn # single column
        self.rowct=0                       # row count
        self.linect=0                      # line count
        self.rows=[]                       # list of rows
        self.rules=[]                      # rows which have rules after
        self.lines=[]                      # list of lines
        self.tracepaths={}                 # trace paths
        self.prev=toprow                   # previous row (for working out traces)

        # add top row
        self.rows.append(toprow)

        # add top row as line
        self.lines.append(toprow)
        self.linect+=1

        # if a leadend add rule below it
        if self.showrule and not(self.rulebefore) and toprow.leadend:
            self.rules.append(self.rowct)
            self.lines.append(None)
            self.linect+=1

        # initialise tracepaths
        for n in self.fmt.tracecolours.keys():
            self.tracepaths[n]=[0]


    ### output column

    def __str__(self):
        txt=''
        for row in self.lines:
            if row is None:
                txt+='%s\n' % self.fmt.rulestr
            else:
                txt+='%s\n' %row
        return txt

    ### addrow - add a row to a column

    def addrow(self,row):

        # add row
        self.rows.append(row)
        self.rowct+=1

        # add line for rule before leadend
        if self.showrule and self.rulebefore and row.leadend:
            self.rules.append(self.rowct-1)
            self.lines.append(None)
            self.linect+=1

        # add line for row
        self.lines.append(row)
        self.linect+=1

        # add line for rule after leadend
        if self.showrule and not(self.rulebefore) and row.leadend:
            self.rules.append(self.rowct)
            self.lines.append(None)
            self.linect+=1

        # extend tracepaths
        for n in self.tracepaths.keys():
            if n<=row.nbells:
                self.tracepaths[n].append(row.places.index(n)-self.prev.places.index(n))
            else:
                self.tracepaths[n].append(0)

        # save row as previous
        self.prev=row


    ### isfull - return True if column is full

    def isfull(self):
        return not(self.singlecolumn) and self.rowct>=self.nrows

    ### removeorphan - remove orphan rule at end of column

    def removeorphan(self):
        if self.lines[-1] is None:
            self.rules.pop()
            self.lines.pop()
            self.linect-=1

    ### typesetline - typeset a line for printing

    def typesetline(self,lineno):

        call=''    # call symbol
        bells=''   # bells
        pn=''      # place notation
        comment='' # comment

        if lineno<self.linect:

            if self.lines[lineno] is None:

                # rule row
                bells=self.fmt.rulestr

            else:

                # real row
                bells=self.lines[lineno].format(self.bellsyms,'',self.nbells)
                if lineno>0:
                    call=self.lines[lineno].call
                    pn=self.lines[lineno].pn
                    comment=self.lines[lineno].comment

        # return content

        txt=''
        if self.fmt.showcall:
            txt+='%-2s' %call
        txt+=bells
        if self.fmt.showpn:
            txt+=' %-*.*s' %(self.nbells-2,self.nbells-2,pn)
        if self.fmt.showcomments:
            txt+=' %-*.*s' %(self.fmt.commentlen,self.fmt.commentlen,comment)
        return txt


    ### typesetcsv - typeset column as CSV

    def typesetcsv(self):

        txt=''

        for row in self.rows:

            if self.fmt.showcall:
                txt+='%s,,' %row.call

            txt+=row.format(self.bellsyms,',',self.nbells)

            if self.fmt.showpn:
                txt+=',,%s' %row.pn

            if self.fmt.showcomments:
                txt+=',,%s' %row.comment

            txt+='\n'

        return txt

