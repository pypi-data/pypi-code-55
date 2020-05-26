######################################################################
### Change Ringing Engine
### Copyright (c) 2020 Jonathan Wilson
### Please refer to help/licence.txt for further information
### File: svg.py
### Description: Typesetting of rows as HTML (SVG)
### Last Modified: 24 May 2020
######################################################################

### typeset - typeset document as SVG

def typeset(doc,fmt):
    html='<html>\n<body>\n'
    for page in doc.pages:
        html+=typeset_page(page,fmt)
    html+='</body>\n</html>\n'
    return html


### typeset_page

def typeset_page(page,fmt):

    # determine page dimensions
    pageheight=fmt.pageheight
    pagewidth=page.colct*fmt.columnwidth
    pagewidth+=(page.colct-1)*fmt.columnsep
    pagewidth+=fmt.leftmargin+fmt.rightmargin

    # begin SVG content
    html='<svg width="%d" height="%d">\n' %(pagewidth,pageheight)
    html+='<rect width="%d" height="%d"' %(pagewidth,pageheight)
    html+='style="fill:none;stroke:black;stroke-width;3" />\n'

    # typeset columns
    for colno,column in enumerate(page.columns):
        html+=typeset_column(column,fmt,colno)

    # end SVG content
    html+='</svg>\n'
    return html


### typeset_column - typeset column as SVG

def typeset_column(column,fmt,colno):

    # start a new column
    html='<g font-size="%s"' %fmt.fontsize
    html+='font-family="sans-serif" fill="#000000" stroke="none">\n'

    html+=svgtext(fmt,colno,0,0,column.rows[0].format(column.bellsyms,'',column.nbells),True)

    for j,row in enumerate(column.rows[1:]):

        if fmt.showcall and row.call!='':
            html+=svgtspan(fmt,colno,j+1,-2,row.call,False)

        html+=svgtspan(fmt,colno,j+1,0,row.format(column.bellsyms,'',column.nbells),True)

        if fmt.showpn and row.pn!='':
            html+=svgtspan(fmt,colno,j+1,column.nbells+1,row.pn,False)

    html+='</text>\n</g>\n'

    # typeset rules
    for r in column.rules:
        html+=svgline(fmt,colno,r,'black',2)

    # typeset tracepaths
    for n in column.tracepaths.keys():

        if n<=column.rows[0].nbells:
            s=column.rows[0].places.index(n)
        else:
            s=n

        html+=svgpolyline(
            fmt,colno,s
            ,column.tracepaths[n]
            ,'#'+fmt.tracecolours[n]
            ,fmt.traceweights[n]
            )

    return html


### svgtext

def svgtext(fmt,colno,rowno,offset,txt,mult):
    xo=getx(fmt,colno,offset)
    yo=gety(fmt,rowno)
    n=len(txt) if mult else 1
    xs=','.join([str(int(xo+i*fmt.charsep)) for i in range(0,n)])
    ys=','.join([str(yo) for i in range(0,n)])
    return '<text x="%s" y="%s">%s\n' %(xs,ys,txt)

### svgtspan

def svgtspan(fmt,colno,rowno,offset,txt,mult):
    xo=getx(fmt,colno,offset)
    yo=gety(fmt,rowno)
    n=len(txt) if mult else 1
    xs=','.join([str(int(xo+i*fmt.charsep)) for i in range(0,n)])
    ys=','.join([str(yo) for i in range(0,len(txt))])
    return '<tspan x="%s" y="%s">%s</tspan>\n' %(xs,ys,txt)


### svgline

def svgline(fmt,colno,rowno,colour,thickness):
    x1=getx(fmt,colno,0)
    x2=getx(fmt,colno,fmt.nbells)
    y=gety(fmt,rowno+0.25)
    return '<line x1="%d" y1="%d" x2="%d" y2="%d" style="stroke:%s;stroke-width:%s" />' %(
        x1,y,x2,y,colour,thickness)
        

### svgpolyline

def svgpolyline(fmt,colno,offset,trace,colour,thickness):

    xo=getx(fmt,colno,-0.5)
    yo=gety(fmt,-0.5)

    xs=[offset+trace[0]]
    for x in trace[1:]:
        xs.append(x+xs[-1])

    pts=' '.join([str(int(xo+x*fmt.charsep))+','
                  +str(int(yo+y*fmt.baselinesep))
                  for y,x in enumerate(xs)])

    return '<polyline points="%s" style="fill:none;stroke:%s;stroke-width:%s" />\n' % (
            pts,colour,thickness)


### getx - get absolute coordinate of a column

def getx(fmt,colno,charno):
    x=fmt.leftmargin
    x+=colno*(fmt.columnwidth+fmt.columnsep)
    x+=charno*fmt.charsep
    return int(x)

### gety - get absolute coordinate of a row

def gety(fmt,rowno):
    y=fmt.topmargin+rowno*fmt.baselinesep
    return int(y)

