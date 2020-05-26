######################################################################
### Change Ringing Engine
### Copyright (c) 2020 Jonathan Wilson
### Please refer to help/licence.txt for further information
### File: postscript.py
### Description: Typesetting of rows
### Last Modified: 24 May 2020
######################################################################

### import modules

from datetime import datetime
from .rowfmt import rgbcolour

### typeset

def typeset(doc,fmt):

    # pagewidth/height - take from format
    pagewidth=fmt.pagewidth
    pageheight=fmt.pageheight

    # adjust pagewidth for single page output
    if fmt.singlepage:
        pagewidth=doc.pages[0].colct*fmt.columnwidth
        pagewidth+=(doc.pages[0].colct-1)*fmt.columnsep
        pagewidth+=fmt.leftmargin+fmt.rightmargin
        fmt.pagewidth=pagewidth

    # postscript header
    ps='%%!PS-Adobe-3.0%s\n' % (' EPSF-3.0' if fmt.singlepage else '')
    ps+='%%Creator: Change Ringing Engine 0.8\n'
    ps+='%%%%Title: %s\n' % doc.title
    ps+='%%%%CreationDate: %s\n' % datetime.now()
    ps+='%%Pages: (atend)\n'
    ps+='%%DocumentFonts: (atend)\n'
    ps+='%%%%BoundingBox: 0 0 %d %d\n' % (pagewidth, pageheight)
    ps+='%%EndComments\n'

    # fonts
    ps+='\n% Page fonts\n'
    ps+='/TextFont /%s findfont %d scalefont def\n' % (
        'Helvetica',fmt.fontsize)
    ps+='/TitleFont /%s findfont %d scalefont def\n' % (
        'Helvetica-Bold',fmt.fontsize)
    ps+='/PnFont /%s findfont %d scalefont def\n' % (
        'Helvetica-Oblique',fmt.fontsize)
    ps+='/CommentFont /%s findfont %d scalefont def\n' % (
        'Helvetica-Oblique',fmt.fontsize)

    # colours
    ps+='\n% Page colours\n'
    ps+='/rulecolour {%s} def\n' % psrgbcolour(fmt.rulecolour)
    ps+='/pncolour {%s} def\n' % psrgbcolour(fmt.pncolour)
    ps+='/commentcolour {%s} def\n' % psrgbcolour(fmt.commentcolour)
        
    # add definitions to prologue
    ps+=ps_prologue_defs

    # add pages
    for pageno,page in enumerate(doc.pages):
        ps+=typeset_page(page,fmt,pageno+1)

    # trailer
    ps+='\n%%Trailer\n'
    ps+='%%DocumentFonts: Helvetica\n'

    return ps


### typeset_page - typeset single page

def typeset_page(page,fmt,pageno):

    ps=''

    # start page unless in singlepage mode
    if not(fmt.singlepage):
        x=fmt.leftmargin
        y=fmt.pageheight-fmt.topmargin-fmt.charsep+2*fmt.baselinesep
        ps+='%%%%Page: %d %d\n' %(pageno,pageno)
        ps+='setlandscape\n' if fmt.landscape else ''
        ps+='(%s) %d %d heading\n' % (page.title,x,y)

    # typeset columns in page
    ps+='TextFont setfont\n'
    for colno,column in enumerate(page.columns):
        ps+=typeset_column(column,fmt,colno)

    # eject page unless in singlepage mode
    if not(fmt.singlepage):
        ps+='showpage\n'

    return ps


### typeset_column - typeset single column

def typeset_column(column,fmt,colno):

    # start column
    ps=''

    # horizontal centre of first place
    xhome=fmt.leftmargin+colno*(fmt.columnwidth+fmt.columnsep)+0.5*fmt.charsep

    # indent if calls are being shown
    #if fmt.showcall:
    #    xhome+=2*fmt.charsep

    # vertical coordinate of top baseline
    yhome=fmt.pageheight-fmt.topmargin-fmt.charsep

    # typeset rows with calls, pn and comments
    x=xhome+0.5*fmt.charsep
    xn=xhome+(fmt.nbells+1)*fmt.charsep
    xc=xn+0.5*int(fmt.showpn)*(fmt.nbells+1)*fmt.charsep
    y=yhome
    
    # top row - bells only
    bells=column.rows[0].format(column.bellsyms,'',column.nbells)
    for b,bell in enumerate(bells):
        ps+='(%s) %d %d bell\n' % (
            bell,x+b*fmt.charsep,y)
    y-=fmt.baselinesep

    # other rows
    for row in column.rows[1:]:

        # call symbol
        if fmt.showcall and row.call!='':
            ps+='(%s) %d %d bell\n' % (
                row.call,x-2*fmt.charsep,y)

        # bells
        bells=row.format(column.bellsyms,'',column.nbells)
        for b,bell in enumerate(bells):
            ps+='(%s) %d %d bell\n' % (
                bell,x+b*fmt.charsep,y)

        # place notation
        if fmt.showpn and row.pn!='':
            ps+='(%s) %d %d pn\n' % (row.pn,xn,y)

        # comments
        if fmt.showcomments and row.comment!='':
            ps+='(%s) %d %d comment\n' % (row.comment,xc,y)

        # move to next row
        y-=fmt.baselinesep

    # add rules
    x0=xhome
    x1=x0+fmt.nbells*fmt.charsep
    y=yhome-0.2*fmt.charsep
    psrgb=psrgbcolour(fmt.rulecolour)
    for r in column.rules:
        ps+='%d %d moveto %d %d lineto %s %d stroketrace\n' % (
            x0,y-r*fmt.baselinesep,x1,y-r*fmt.baselinesep,psrgb,fmt.rulethickness)

    # add traces
    for n in column.tracepaths.keys():

        if n<=column.rows[0].nbells:
            s=column.rows[0].places.index(n)
        else:
            s=n

        x=xhome+fmt.charsep*(s-0.5)
        y=yhome+0.5*fmt.charsep
        ps+='%d %d moveto\n' %(x,y)

        for d in column.tracepaths[n][1:]:
            x+=d*fmt.charsep
            y-=fmt.baselinesep
            ps+='%d %d lineto\n' %(x,y)

        psrgb=psrgbcolour(fmt.tracecolours[n])
        thickness=fmt.traceweights[n]
        ps+='%s %d stroketrace\n' %(psrgb,thickness)

    # end of column
    return ps


### psrgbcolour - convert colour to rgb (postscript)

def psrgbcolour(s):
    (r,g,b)=rgbcolour(s)
    r1=round(r/255.0,3)
    g1=round(g/255.0,3)
    b1=round(b/255.0,3)
    return '%.2f %.2f %.2f' %(r1,g1,b1)


### ps_prologue_defs - definitions to be placed in postscript prologue

ps_prologue_defs='''
% Landscape
/setlandscape {pageheight 0 translate 90 rotate} def

% show heading
/heading {
    moveto
    currentfont
    exch
    TitleFont setfont
    show
    setfont
} def

% Display bell character
/bell { moveto dup stringwidth pop -0.5 mul 0 rmoveto show } def

% Display place notation
/pn {
    moveto
    currentrgbcolor
    currentfont
    5 -1 roll
    pncolour setrgbcolor
    CommentFont setfont
    show
    setfont
    setrgbcolor
} def

% Display comment
/comment {
    moveto
    currentrgbcolor
    currentfont
    5 -1 roll
    commentcolour setrgbcolor
    CommentFont setfont
    show
    setfont
    setrgbcolor
} def

% Coloured trace
/stroketrace {
    currentrgbcolor
    currentlinewidth
    8 -4 roll
    setlinewidth
    setrgbcolor
    stroke
    setlinewidth
    setrgbcolor
} def

%%EndProlog
'''

