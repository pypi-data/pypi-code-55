#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 16:39:19 2019

@author: stephan
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 20:44:38 2018

@author: Stephan Rein
"""

from PyQt5.QtWidgets import QVBoxLayout, QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigCanv
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as bar
from matplotlib.figure import Figure
from PyQt5 import QtGui, QtCore
import matplotlib
import numpy as np
import warnings as warnings
warnings.filterwarnings("ignore")


class MplCanvas(FigCanv):
    def __init__(self, figure):
        FigCanv.__init__(self, figure)
        FigCanv.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigCanv.updateGeometry(self)
# HERE CHANGE THE COLOR OF ZOOM RECTANGLE
    def drawRectangle(self, rect):
        if rect is not None:
            def _draw_rect_callback(painter):
                # IN THIS EXAMPLE CHANGE BLACK FOR WHITE
                pen = QtGui.QPen(QtCore.Qt.white, 1 / self._dpi_ratio,
                             QtCore.Qt.SolidLine)
                painter.setPen(pen)
                painter.drawRect(*(pt / self._dpi_ratio for pt in rect))
        else:
            def _draw_rect_callback(painter):
                return
        self._draw_rect_callback = _draw_rect_callback
        self.update()


def figure_handler_init(s):
#    QWidget.__init__(self, parent)
    FigCanv.setSizePolicy(s, QSizePolicy.Expanding, QSizePolicy.Expanding)
    s.figure = Figure()
    s.figure.set_facecolor("black")
    s.canvas = MplCanvas(s.figure)
    s.bar = bar(s.canvas, s)
    s.layout = QVBoxLayout(s.Plot_window)
    s.layout.addWidget(s.canvas)
    s.layout.addWidget(s.bar)
    s.ax = s.figure.add_subplot(111)
    s.ax.set_yticks([])
    s.ax.set_xticks([])
    check_color_settings(s, s.figure, s.ax)
    s.canvas.draw()
    return


def check_color_settings(s, fig, ax):
    fig.set_facecolor("black")
    ax.set_facecolor("black")
    ax.yaxis.label.set_color("white")
    ax.xaxis.label.set_color("white")
    ax.title.set_color("white")
    ax.tick_params(axis='x', colors="white")
    ax.tick_params(axis='y', colors="white")
    ax.spines['bottom'].set_color("white")
    ax.spines['top'].set_color("white")
    ax.spines['right'].set_color("white")
    ax.spines['left'].set_color("white")
    matplotlib.rcParams['text.color'] = "white"
    return


def set_axislabel(s, ax):
    ax.set_xlabel("$magnetic\, field\, / \, \mathrm{mT}$", size=int(s.fonts+1))
    ax.set_ylabel("$intensity$", size=int(s.fonts+1))
    return


def define_figure(s, ax, n, m=None):
    if m is None:
        m = n
    ax.clear()
    ax = s.figure.add_subplot(111)
    ax.set_autoscaley_on(False)
    ax.axis('on')
    return


def do_ticks(ax, fonts):
    for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize(fonts)
    for tick in ax.yaxis.get_major_ticks():
        tick.label.set_fontsize(fonts-1)
    return


def define_y_axis(ax, ydata, k, g=None):
    if g is None:
        g = k
    k = k*0.01
    g = g*0.01
    diff = np.max(ydata)-np.min(ydata)
    ax.set_ylim([np.min(ydata)-k*diff, np.max(ydata)+g*diff])
    return


def define_x_axis(ax, xdata, facr=1, facl=1, Range=None):
    if Range is None:
        ax.set_xlim([np.min(xdata)/facl, np.max(xdata)/facr])
    else:
        ax.set_xlim([Range[0], Range[1]])
    return


def textposition(x, y):
    miny = np.min(y)
    maxy = np.max(y)
    minx = np.min(x)
    maxx = np.max(x)
    diffx = maxx-minx
    x = minx+0.03*diffx
    diffy = maxy-miny
    y = maxy - 0.05*diffy
    return x, y


def figure_handler(s, xdata, ydata, multi=False):
    # PELDOR time trace
    define_figure(s, s.ax, 0)
    try:
        define_y_axis(s.ax, ydata, 8)
    except ValueError:
        pass
    define_x_axis(s.ax, xdata)
    do_ticks(s.ax, int(s.fonts))
    set_axislabel(s, s.ax)
    if not multi:
        s.ax.plot(xdata, ydata, color=s.tracecolor)
        #s.ax.plot(xdata, np.zeros(len(xdata)), '--',  color='white')
    else:
        for i in range(0, len(xdata)):
            if i == 0:
                colors = s.tracecolor
            else:
                colors = "magenta"
            s.ax.plot(xdata[i], ydata[i], color=colors)
        s.ax.plot(xdata[0], np.zeros(len(xdata[0])), '--', color='r')
    s.figure.tight_layout()
    s.canvas.draw()
    return


def figure_handler_fit(s, xdata, ydata, xdata2, ydata2, multi=False):
    # PELDOR time trace
    define_figure(s, s.ax, 0)
    define_y_axis(s.ax, np.concatenate((ydata,ydata2)), 8)
    define_x_axis(s.ax, np.concatenate((xdata, xdata2)))
    do_ticks(s.ax, int(s.fonts))
    set_axislabel(s, s.ax)
    s.ax.plot(xdata2, ydata2, color=s.tracecolor)
    s.ax.plot(xdata, ydata, color=s.tracecolor_fit)
    try:
        x1, y1  = textposition(xdata, np.concatenate((ydata, ydata2)))
        str_tmp =  "Sum of least squares: \n" + str(round(s.objective, 5))
        s.ax.text(x1, y1, str_tmp)
    except:
        pass
    s.ax.legend(['exp','sim'], loc=1,facecolor="black")
    s.figure.tight_layout()
    s.canvas.draw()
    return
