# -*- coding: utf-8 -*-
""" 
The ember module contains the basis elements to build IPCC-style 'burning ember diagrams'
Copyright (C) 2020  philippe.marbaix@uclouvain.be
"""

import numpy as np
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib import colors as col
from reportlab.lib.units import mm
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import os
servpath = os.path.dirname(globals()['__file__'])
from embermaker import helpers as hlp

def skeygroup(be):
    global sortlist
    """
    Used for sorting embers by group. If sortlist is defined, try to use the order defined in this list
    :param be: an ember object
    :return: sort key
    """
    if len(sortlist) > 1:
        try:
            pos = sortlist.index(be.group.lower())
        except(ValueError):
            pos = 0
    else:
        pos = be.group
    return pos

def skeyname(be):
    global sortlist
    """
    Used for sorting embers by name. If sortlist is defined, try to use the order defined in this list
    :param be: an ember object
    :return: sort key
    """
    if len(sortlist) > 1:
        try:
            pos = sortlist.index(be.name.lower())
        except(ValueError):
            pos = 0
    else:
        pos = be.name
    hlp.addlogmes("Sort key for:" + str(be.name.lower()) + "->" + str(pos))
    return pos


def cbyinterp(rlev, csys, cdefs):
    """
    Provides a color by interpolating between the defined color levels associated to risk levels
    :param rlev: the risk level for which a color is requested
    :param csys: the name of the color system (currently CMYK or RGB)
    :param cdefs: the definition of the colors associated to risk levels, such that
         - cdefs[0] : a risk level index (1D numpy array of risk indexes)
         - cdefs[1:]: the color densities for each value of the risk index :
                    (1D numpy array of color densities for each risk index)
    :return: the color associated to the risk level
    """
    cvals = [np.interp(rlev, cdefs[0], cdefs[1+i]) for i in range (len(csys)) ]
    if csys == 'CMYK':
        c,m,y,k = cvals
        thecol = col.CMYKColor(c,m,y,k)
    elif csys == 'RGB':
        r,g,b = cvals
        thecol = col.Color(r,g,b, alpha=1.0)
    else:
        raise Exception("Undefined color system")
    return thecol

def isempty(value):
    """
    Finds if a variable is "empty", whatever the type and including strings containing blanks
    :param value: the data to be checked
    :return: whether the input value is judged 'empty'
    """
    if value == []:
        return True
    if isinstance(value, str):
        if value.strip() == u'':
            return True
    return False

def stripped(value):
    """
    Remove blanks if the value is a string, don't touch if it is not a string:
    :param value: the string to be processed
    :return: the 'stripped' string
    """
    if isinstance(value, str):
        return value.strip()
    else:
        return value

class Ember(object):
    """ An ember is one set of data in a "burning embers" diagram.
        It contains hazard levels and associated risk levels, as well as the 'draw' method to plot itself.
    """

    def __init__(self): #Todo: consider removing ?
        """
        Initializes an ember, by creating standard attribute so that creating other attributes
        may generate a warning.
        """
        # Attributes: (see __setattr__ below)
        self.name = ""
        self.group = ""
        self.risk = None
        self.hazl = None
        self.conf = None
        self.toph = None
        self._inited= True

    def __setattr__(self, key, value):
        """
        Force explicit declaration of attributes, as a precaution measure against typos in the calling code.
        Will issue a warning if an attribute is created after initialisation.
        May remove if jugged unsefull (but it makes no harm in this context :-).
        :param key: the name of the attribute to change
        :param value: the value to be given to the attribute
        """
        if hasattr(self, '_inited') and not hasattr(self, key):
            hlp.addlogwarn("Creating ember attribute which was not defined at initialization: " + key)
            # Thanks to https://stackoverflow.com/questions/3603502/prevent-creating-new-attributes-outside-init
        object.__setattr__(self, key, value)

    def draw(self, egr, xpos, ypos=None):
        """
        Draws an ember
        :param egr: an ember graph (including the canvas to draw to and methods that deal with the entire graph)
        :param xpos: the x coordinates that define the ember's drawing area [x0, width]
        :param ypos: to draw a legend, the y coordinates of the ember's drawing area [y0, height].
                     ypos can only be set to draw the legend, because the y coordinates of embers
                     are taken for egr for consistency with the y-axis.
        """
        hlp.addlogmes('Drawing ember: '+self.name)
        c = egr.c
        plotlevels = []
        colorlevels = []

        # Variable names:
        # sx, sy
        # ty

        bx, sx = xpos
        if ypos != None: # Non-standard case: to plot the colour bar (legend), outside of the current coordinates
            by, sy = ypos
            rscale = [np.min(self.hazl), np.max(self.hazl)]
            ygmin = 0
            ygmax = 1
            ty = sy
        else: # Standard case - to plot an ember according to the current coordinates
            rscale = None
            ygmin = egr.scale(0) # Starting point for the gradients
            ygmax = egr.scale(max(np.max(self.hazl), self.toph)) # End point for the gradients
            by = egr._y0
            sy = egr._y
            ty = min(egr.scale(self.toph), sy)

        #To ensure full consistency, all hazard values are converted to canvas coordinates, and divided
        #by the range of each gradient when plotting a gradient.

        # y range (height on the canevas) of the gradient:
        yran = ygmax - ygmin

        for ihaz in range(len(self.risk)):
            # Fractional position within a gradient of each colour change
            plotlevels.append((egr.scale(self.hazl[ihaz], rscale = rscale) - ygmin) / yran)
            # Associated colour
            col = cbyinterp(self.risk[ihaz], egr.csys, egr.cdefs)
            colorlevels.append(col)
        # Copy the start and end colors at both ends of the plot range
        # (= extend the last colour beyond the last transition):
        plotlevels.append(1.0)
        colorlevels.append(colorlevels[-1])
        plotlevels.insert(0, 0)
        colorlevels.insert(0, colorlevels[0])  # top (copy the last available colour to the 'top' level)

        hlp.addlogmes(plotlevels)
        hlp.addlogmes(colorlevels)

        # Set linewidth for the box around the ember:
        lineWidth = 0.3*mm
        c.setLineWidth(lineWidth)
        c.setStrokeColor(egr.black)
        # Draw ember background (= no data)
        c.setFillColor(egr.vlgrey)
        c.rect(bx, by, sx, sy, stroke=0, fill=1)

        c.saveState() # to be able to revert to the current drawing context after drawing the gradients.
        # Restrict the viewable area to the frame enclosing the BE
        # (colour gradients do not have x limits, hence the need to limit their visible part):
        p = c.beginPath()
        p.rect(bx, by, sx, ty)
        c.clipPath(p, stroke=0)

        # Plot the BE gradients
        if ypos == None: # Standard case - ember: only vertical is supported for the moment
            c.linearGradient(bx, by+ygmin, bx, by+ygmax, colorlevels, plotlevels, extend=False)
        else:   # Legend
            if sx > sy: # Horizontal gradient
                c.linearGradient(bx, by, sx+bx, by, colorlevels, plotlevels, extend=False)
            else:       # Vertical gradient
                c.linearGradient(bx, by, bx, sy+by, colorlevels, plotlevels, extend=False)

        # Revert back to the normal viewable area
        c.restoreState()

        # Plot the box around the BE:
        c.setStrokeColor(egr.black)
        c.rect(bx, by, sx, sy, stroke=1, fill=0)
        c.setFillColor(egr.black)

        # Add the name of the BE
        # - - - - - - - - - - -
        thestyle = egr.style
        thestyle.alignment = TA_CENTER
        thestyle.fontSize = egr.getgp('fnt_size')
        thestyle.leading = thestyle.fontSize
        P = Paragraph(self.name, thestyle)
        # This calculate the height needed to render the paragraph, it is the only way to get it
        # vertically aligned to "top" (= right under the graphic)
        w, h = P.wrap(egr.getgp('be_x') + egr.getgp('be_int_x'), egr.getgp('be_bot_y')) #ToDo
        P.drawOn(c, bx - egr.getgp('be_int_x') / 2, by - h)

        return (bx + egr.getgp('be_x') / 2)

class EmberGraph(object):
    """
    EmberGraphs stores the general information on a graphic containing embers,
    and provides methods for drawing such graphs (except for the embers themselves, which are dealt with
    in the Ember class)
    We have included the creation of the drawing canvas here because we want to perfom some intialisation
    before the main program can access the canvas; before that, it could draw RGB color on an otherwise CMYK figure,
    now the main drawing parameters are set here to prevent that.
    """

    def __init__(self, outfile, csys, cnames, cdefs, gp):
        self.csys = csys
        self.cdefs = cdefs
        self.csys  = csys
        self.cdef  = cdefs
        self.cnames= cnames
        self.gp = gp

        # Define the drawing canvas
        self.c = Canvas(outfile, enforceColorSpace=self.csys)  # drawing canevas
        # Define colors for texts and lines according to the color system;
        # a PDF may contain several color systems at the same time, hence this seems to provide consistency.
        if csys == "CMYK":
            self.black = col.CMYKColor(0, 0, 0, 1) # Standard black, for texts and lines
            self.blue  = col.CMYKColor(1, 0.4, 0, 0)
            self.grey  = col.CMYKColor(0, 0, 0, 0.4)
            self.red   = col.CMYKColor(0, 0.88, 0.85, 0)
            self.vlgrey= col.CMYKColor(0, 0, 0, 0.1) # Very light grey
            self.tgrey = col.CMYKColor(0, 0, 0, 1, alpha=0.5) # Transparent grey
            self.tdarkgrey = col.CMYKColor(0, 0, 0, 1, alpha=0.7) # Transparent dark grey
            self.white = col.CMYKColor(0, 0, 0, 0)
        else:
            self.black = col.Color(0, 0, 0)
            self.blue  = col.Color(0, 0, 1)
            self.grey  = col.Color(0.6,0.6,0.6)
            self.red   = col.Color(1,0,0)
            self.vlgrey= col.Color(0.9,0.9,0.9) # Very light grey
            self.tgrey = col.Color(0, 0, 0, alpha=0.5)
            self.tdarkgrey = col.Color(0, 0, 0, alpha=0.7) # Transparent dark grey
            self.white = col.Color(1, 1, 1)

        self.c.setStrokeColor(self.black)
        self.c.setFillColor(self.black)

        # text paragraphs styles
        styleSheet = getSampleStyleSheet()
        self.style = styleSheet['BodyText']
        self.style.fontName = gp['fnt_name']
        self.style.fontSize = gp['fnt_size']
        self.style.alignment = TA_CENTER
        self.style.leading = 10
        self.c.setFont(gp['fnt_name'], gp['fnt_size'])

    def getgp(self, gpname, data=False, vtype=None, default=''):
        """
        Gets the value of a gp (graphic parameter from a dictionnary);
        if parameter is empty or not defined and default exists, return default (if no default, return empty string)
        if data=True and the value is not a list with more then 1 element, return default (if no default, return [])
        if only one value, which is text, pass as is.
        if only one value, which is number, pass as float
        if two values, of which the first is number and the second is 'cm', pass float(value[0])*cm (units = cm)
        if list, by default pass element [0];
        if list and data=True, pass the 'data' part of the parameter: anything beyond element 0.
        :param gpname: the name of the parameter
        :param data: if the parameter is a list of values and data=True, return the 'data part' of the parameter
        :param vtype: lower => must be a string, will be converted to lower case;
                      float => check that it is a float or can be converted
        :return: value of the parameter (converted to float if it is a number)
        """
        if gpname not in self.gp.keys():
            hlp.addlogmes("Graph parameter '" + str(gpname) + "' is undefined.")
            val = default
            return val
            
        val = self.gp[gpname]
        if isempty(val):
            val = default
        elif data and (not isinstance(val, list) or len(val) < 2):
            if default == '':
                val = []
            else:
                val = default
            return val
        elif isinstance(val,str):
            val = val.strip()
            if vtype== 'lower':
                val = val.lower()
        elif not isinstance(val,list):
            val = float(val)
        elif len(val) == 2 and stripped(val[1]) == 'cm':
            val = float(val[0]) * cm
        elif data: # Todo: this part is now too complex, the entire getgp would benefit from revision => more simplicity
            if vtype== 'lower':
                val = [str(v).strip().lower() for v in val[1:]]
            else:
                val = val[1:]
        else:
            if len(val) > 1:
                val = val[0]
                if isempty(val):
                    val = default
                if vtype== 'lower':
                    if isinstance(val,str):
                        val = val.strip().lower()
                    else:
                        raise Exception("This parameter should be a string: " + str(gpname) + "=>" + str(val))
            else:
                val = []

        if vtype == 'float':
            try:
                if type(val) == list:
                    val = [float(v) for v in val]
                else:
                    val = float(val)
            except:
                raise Exception("This parameter should be a number: " + str(gpname) + "=>" + str(type(val)))

        #hlp.addlogmes(str(gpname)+'=>'+str(type(val)))
        return val

    def isdefined(self, gpname):
        if gpname not in self.gp:
            return False
        else:
            return not isempty(self.gp[gpname])

    def pincoord(self, be_y0, be_y):
        """
        Establishes the correspondance between hazard values and 'physical' coordinates on the canvas.
        To avoid potential inconsistencies, the coordinates should be changed only with this function, so that
        every use of the scale function below provides a result with the same mapping from hazard to canvas.
        Note: be_y0, be_y0+be_y define the drawing area on the canvas and correspond to haz_bottom_value, haz_top_value;
        (however it is permitted to enter data outside the haz_ range, they will remain invisble but may have
        a visible impact trough interpolation from a visible data point)
        :param be_y0: bottom of the drawing area on the canvas
        :param be_y: height of the drawing area on the canvas
        """
        # All of the following are 'protected' variables: they should not be changed from outside the EmberGraph class.
        self._protected = ()
        self._y0 = be_y0
        self._y = be_y
        self._hz0 = self.gp['haz_bottom_value']
        self._hz1 = self.gp['haz_top_value']
        self._hz = self._hz1 - self._hz0
        self._protected = ('_y0', '_y', '_hz0', '_hz1', '_hz')

    def __setattr__(self, key, value):
        """
        Enforces protection of a tuple of protected variables when changing attributes
        :param key: the name of the attribute to be changed
        :param value: the value of the attribute to be change
        """
        if hasattr(self, '_protected') and key in self._protected:
            raise Exception("Attempt at changing a protected variable (set by pincoord): " + str(key))
        object.__setattr__(self, key, value)

    def scale(self, hazvalue, rscale=None):
        """
        :param hazvalue: a value on the y-axis (hazard axis, e.g. temperature)
        :param rscale: [bottom value, top value] of a specific axis (needed for the legend);
                       the default values were set by pincoord = for the active drawing y-coordinates/area.
        :return: the result of the scaling to the y canevas coordinates
        """
        if rscale is None:
            hz0 = self._hz0
            hz  = self._hz
            y   = self._y
        else:
            # this is to allow drawing the legend: avoid using the hazard scale from gp parameters
            hz0 = rscale[0]
            hz  = rscale[1] - rscale[0]
            y   = 1.0
        return y * (hazvalue - hz0) / hz

    def vaxis(self, xpos):
        # plot 'hazard' axis : grid lines and values
        # The x coordinates are variable because they define the position and width of the axis;
        bx, sx = xpos
        # The y coordinates are fixed by the data from pincoord because they must be consistent with the ember
        by = self._y0

        self.c.setLineWidth(0.5 * mm)
        self.c.setStrokeColor(self.grey)

        glines, labfmt = hlp.nicelevels(self.gp['haz_bottom_value'], self.gp['haz_top_value'],
                                    nalevels = self.getgp('haz_grid_lines', default=6), enclose = False)


        # Self defined grid lines (from nicelevels above):
        lbx = bx + self.getgp('scale_x')
        sbx = bx + 0.92 *self.getgp('scale_x')
        for haz in glines:
            yp = by + self.scale(haz)
            self.c.line(lbx, yp, bx + sx, yp)
            self.c.drawRightString(sbx, yp - 1 * mm, labfmt.format(haz) + self.getgp('haz_unit'))

        # Add any user-defined specific grid lines (done separetely due to different formatting method)
        if self.isdefined('haz_grid_lines'):
            if not isempty(self.getgp('haz_grid_lines', data=True)):
                for haz in self.getgp('haz_grid_lines', data=True, vtype="float"):
                    yp = by + self.scale(haz)
                    self.c.line(lbx, yp, bx + sx, yp)
                    self.c.drawRightString(sbx, yp - 1 * mm, str(haz) + self.getgp('haz_unit'))

    def drawlegend(self, emberbox, isinside):
        """
        Draws a legend (colour bar)
        :param emberbox: a box representing the ember diagram area to which the legend needs to be attached OR
                         in which the legend needs to be drawn
        :param isinside: True if the legend needs to be inside emberbox,
                         False if it needs to be attached outside emberbox
                         (needed because isinside is decided together with emberbox, it is not an input parameter)
        :return: additional horizontal space that is needed because it is occupied by the legend.
        """
        c = self.c
        getgp = self.getgp
        if getgp('leg_pos') in ['under','in-grid-horizontal']:
            ishoriz = True
        else:
            ishoriz = False
            if getgp('leg_pos') not in ['right','in-grid-vertical']:
                hlp.addlogwarn("Parameter leg_pos has an unknown value: " + str(getgp('leg_pos')))

        # Burning ember used as legend:
        be = Ember()
        rlevels = self.cdefs[0]
        # include each level twice to have color transiton + uniform area:
        be.hazl = np.arange(len(rlevels) * 2, dtype=float)
        be.risk = np.repeat(rlevels,2)
        be.toph = be.hazl[-1]

        # Intermediate variables for the position of the legend

        # Size of the legend area
        # Here x and y are in 'legend coordinates', ie x is along the main axis of the legend (vertical OR horizontal)
        ltot_y_h = getgp('leg_bot_y') + getgp('leg_y') + getgp('leg_top_y')
        # For vertical embers, the width depends on the (drawn) length of the risk level names:
        l_cnames = max((c.stringWidth(name, getgp('fnt_name'), getgp('fnt_size')) for name in self.cnames))
        ltot_y_v = getgp('leg_y') + getgp('leg_bot_y') + max(l_cnames, getgp('leg_top_y'))
        ltot_y = ltot_y_h if ishoriz else ltot_y_v
        ltot_x = getgp('leg_x')
        # Allow the text to extend up to 10% beyond the ember on each side
        # (better could be done if needed, this is a rough trick to have a slightly better design):
        ltot_xtext = ltot_x * 0.2

        # Extension of the canvas space when the legend is outside the current graphic area (=> addright):
        if isinside and ishoriz: # in-grid-horizontal: needs to increase the size of emberbox if too small !
            addright = max (0.0, ltot_x + ltot_xtext - emberbox[2]) # by how much is the legend wider than emberbox ?
            emberbox[2] += addright
        elif not (isinside or ishoriz): # legend on the right : entirely in additional space, but outside emberbox.
            addright = ltot_y
        else:
            addright = 0.0 # (under or in-grid-vertical)

        # Center of emberbox
        boxmid = ((emberbox[0] + emberbox[2]/2.0), (emberbox[1]+emberbox[3]/2.0))
        # Center of the legend area
        lmid_x = boxmid[0] if (ishoriz or isinside) else (emberbox[0]+emberbox[2]+ltot_y/2.0)
        lmid_y = boxmid[1] if (isinside or not ishoriz) else (emberbox[1] - ltot_y/2.0)

        # Position of the legend's burning ember (basis for the entire legend):
        # Here xpos, ypos are in canvas coordinates.
        if ishoriz:
            xpos = [lmid_x - ltot_x/2.0, ltot_x]
            ypos = [lmid_y - ltot_y/2.0 + getgp('leg_bot_y'), getgp('leg_y')]
        else: # vertical legend
            xpos = [lmid_x - ltot_y/2.0, getgp('leg_y')] # the ember is on the left of the legend
            ypos = [lmid_y - ltot_x/2.0, ltot_x]

        # Draw the ember:
        be.draw(self, xpos, ypos=ypos)

        # Draw the text of the legend and connect text to colors with lines

        # Prepare for drawing lines
        c.setStrokeColor(self.black)
        c.setFillColor(self.black)
        c.setLineWidth(0.5*mm)
        c.setFontSize(40.0 / len(rlevels))
        # Position of the lines (link between ember and risk level) relative to the 'ember'
        xlines = (0.5 + 2 * np.arange(len(rlevels))) / be.toph * self.getgp('leg_x')
        # Prepare for drawing the title of the legend as a paragraph
        st = self.style
        st.fontSize = getgp('fnt_size')
        st.textColor = self.black
        # Draw the lines, name of risk levels, and title of paragraph
        if ishoriz:
            for i, xline in enumerate(xlines):
                c.line(xpos[0]+xline, ypos[0]-getgp('leg_bot_y') * 0.4, xpos[0]+xline, ypos[0]+ypos[1]/ 2)
                c.drawCentredString(xpos[0]+xline, ypos[0]-getgp('leg_bot_y') * 0.8, self.cnames[i])
            if getgp('leg_title'):
                st.alignment = TA_CENTER
                P = Paragraph(getgp('leg_title'), st)
                P.wrap(ltot_x + ltot_xtext, 10 * cm) # The max height doesn't matter
                P.drawOn(c, xpos[0]-ltot_xtext/2.0, ypos[0] + ypos[1] + getgp('leg_top_y') * 0.55)
        else: # Vertical ember
            for i, xline in enumerate(xlines):
                c.line(xpos[0]+xpos[1]/2.0, ypos[0]+xline, xpos[0]+xpos[1]+getgp('leg_bot_y')*0.5, ypos[0]+xline)
                c.drawString(xpos[0]+xpos[1]+getgp('leg_bot_y')*0.6, ypos[0]+xline - 1*mm, self.cnames[i])
            if getgp('leg_title'):
                st.alignment = TA_LEFT
                P = Paragraph(getgp('leg_title'), st)
                P.wrap(ltot_y, 10 * cm) # The max height doesn't matter
                P.drawOn(c, xpos[0], ypos[0]+ypos[1]+getgp('leg_x')*0.05)

        # Return the horizontal length added to the the draw area in the canvas.
        return addright