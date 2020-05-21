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
        self.inited= True

    def __setattr__(self, key, value):
        # in Python, attributes do not need to be defined within the class.
        # Here I prefer to declare them explicitly. The purpose of this addition to __setattr__ is
        # that it will issue a warning if an attribute that was not initialized above is created.
        # I hope that this will help identifying possible typos.
        if hasattr(self, 'inited') and not hasattr(self, key):
            hlp.addlogwarn("Creating ember attribute which was not defined at initialization: " + key)
            # Thanks to https://stackoverflow.com/questions/3603502/prevent-creating-new-attributes-outside-init
        object.__setattr__(self, key, value)

    def draw(self, egr, box, tobox=False):
        """
        Draws an ember
        :param egr: an ember graph (including the canvas to draw to and methods that deal with the entire graph)
        :param box:
        :param tobox:
        """
        hlp.addlogmes('Drawing ember: '+self.name)
        c = egr.c
        plotlevels = []
        colorlevels = []

        bx, by, sx, sy = box
        if tobox: # Non-standard case: to plot the colour bar (legend), outside of the current coordinates
            rscale = [np.min(self.hazl), np.max(self.hazl)]
            ygmin = 0
            ygmax = 1
            ty = sy
        else: # Standard case - to plot an ember according to the current coordinates
            rscale = None
            ygmin = egr.scale(0) # Starting point for the gradients
            ygmax = egr.scale(max(np.max(self.hazl), self.toph)) # End point for the gradients
            by = egr.y0
            ty = min(egr.scale(self.toph), sy)

        #to ensure full consistency, all hazard values are converted to canvas coordinates, and divided
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
        if not tobox: # Standard case - ember: only vertical is supported for the moment
            c.linearGradient(bx, by+ygmin, bx, by+ygmax, colorlevels, plotlevels, extend=False)
        else:         # Caption - only horizontal is supported for the moment
            c.linearGradient(bx, by, sx+bx, by, colorlevels, plotlevels, extend=False)

        # Revert back to the normal viewable area
        c.restoreState()

        # Plot the box around the BE:
        c.setStrokeColor(egr.black)
        c.rect(bx, by, sx, sy, stroke=1, fill=0)
        c.setFillColor(egr.black)

        # Add text about the BE
        # - - - - - - - - - -  -
        thestyle = egr.style
        thestyle.alignment = TA_CENTER
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
                      float => check that it is a float or can be converted?
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
        self.y0 = be_y0
        self.y = be_y
        self.hz0 = self.gp['haz_bottom_value']
        self.hz1 = self.gp['haz_top_value']
        self.hz = self.hz1 - self.hz0

    def scale(self, hazvalue, rscale=None):
        """
        :param hazvalue: a value on the y-axis (hazard axis, e.g. temperature)
        :param rscale: [bottom value, top value] of a specific axis (needed for the caption);
                       the default values were set by pincoord = for the active drawing y-coordinates/area.
        :return: the result of the scaling to the y canevas coordinates
        """
        if rscale is None:
            hz0 = self.hz0
            hz  = self.hz
            y   = self.y
        else:
            # this is to allow caption plotting: avoid using the hazard scale from gp parameters
            hz0 = rscale[0]
            hz  = rscale[1] - rscale[0]
            y   = 1.0
        return y * (hazvalue - hz0) / hz

    def vaxis(self, box):
        # plot 'hazard' axis : grid lines and values
        bx, by, sx, sy = box
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

    def drawcaption(self, botleft):
        # botleft is the bottom-left corner of the caption, as [x,y]; other graph metrics are in the gp dictionnary
        c = self.c
        gp = self.gp
        blx, bly = np.array(botleft)

        # Burning ember used as caption:
        be = Ember()
        rlevels = self.cdefs[0]
        # include each level twice to have color transiton + uniform area:
        be.hazl = np.arange(len(rlevels) * 2, dtype=float)
        be.risk = np.repeat(rlevels,2)
        be.toph = be.hazl[-1]
        rscale  = np.array([0, be.toph]) # Todo: remove?

        # Define the box surrounding this burning ember and draw:
        box=[blx, bly + self.getgp('leg_bot_y'), self.getgp('leg_x'), self.getgp('leg_y')]
        be.draw(self, box, tobox=True)

        # Draw caption text and connect text to colors with lines:
        c.setStrokeColor(self.black)
        c.setFillColor(self.black)
        c.setLineWidth(0.5*mm)
        c.setFontSize(40.0 / len(rlevels))
        linex = blx + (0.5 + 2 * np.arange(len(rlevels))) / rscale[1] * self.getgp('leg_x')
        for i, temp in enumerate(linex):
            c.line(temp, bly + self.getgp('leg_bot_y') * 0.6, temp, bly + self.getgp('leg_bot_y') + self.getgp('leg_y') / 2)
            c.drawCentredString(temp, bly + self.getgp('leg_bot_y') * 0.2, self.cnames[i])
