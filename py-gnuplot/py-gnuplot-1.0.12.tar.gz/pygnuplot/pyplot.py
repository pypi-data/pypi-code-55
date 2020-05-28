#!/usr/bin/env python3
#coding=utf8
"""
Gnuplot for python
"""

from pygnuplot import gnuplot
import sys, string, types
import collections
import subprocess
#import numpy as np  
import pandas as pd

def test():
    print("gplfinance.test()")

def make_splot(data, *args, **kwargs):
    subplot = {'data': data,
            'subtype': 'splot',
            'cmd': []}
    subplot["attribute"] = collections.OrderedDict()

    for v in args:
        subplot["cmd"].append(v)
    for k,v in kwargs.items():
        subplot["attribute"][k] = v
    return subplot

def make_plot(data, *args, **kwargs):
    subplot = {'data': data,
            'subtype': 'plot',
            'cmd': []}
    subplot["attribute"] = collections.OrderedDict()

    for v in args:
        subplot["cmd"].append(v)
    for k,v in kwargs.items():
        subplot["attribute"][k] = v
    return subplot

def multiplot(*args, **kwargs):
    g = gnuplot.Gnuplot()

    for k,v in kwargs.items():
        #print('set %s %s' %(k, v))
        g.cmd('set %s %s' %(k, v))
    if 'multiplot' not in kwargs.keys():
        g.cmd('set multiplot')

    for subplot in args:
        for k,v in subplot["attribute"].items():
            if isinstance(v, list):
                for i in v:
                    #print('set %s %s' %(k, i))
                    g.cmd('set %s %s' %(k, i))
            else:
                #print('set %s %s' %(k, v))
                g.cmd('set %s %s' %(k, v))
        cmd = subplot["cmd"]

        # Conver the data to string format:
        if isinstance(subplot["data"], pd.DataFrame):
            content = subplot["data"].to_csv(sep = ' ')
        else:
            content = str(data)
        g.cmd('$Mydata << EOD\n%s\nEOD' %(content))
        c = subplot["subtype"]
        for cmd in subplot["cmd"]:
            c += ' $Mydata %s, ' %(cmd)
        #print(c)
        g.cmd(c)
        # multiplot automatically unset all the label after one subplot.
        g.cmd('unset for [i=1:50] label i')
    g.reset()

def plot(data, *args, **kwargs):
    __gnuplot(data, "plot", *args, **kwargs)

def splot(data, *args, **kwargs):
    __gnuplot(data, "splot", *args, **kwargs)

def __gnuplot(data, plot_cmd, *args, **kwargs):
    g = gnuplot.Gnuplot()

    # kwargs input:
    for k,v in kwargs.items():
        #print('set %s %s' %(k, v))
        #g.set(**kwargs)
        if isinstance(v, list):
            for i in v:
                #print('set %s %s' %(k, i))
                g.cmd('set %s %s' %(k, i))
        else:
            #print('set %s %s' %(k, v))
            g.cmd('set %s %s' %(k, v))

    # Conver the data to string format:
    if isinstance(data, pd.DataFrame):
        content = data.to_csv(sep = ' ')
    else:
        content = str(data)
    g.cmd('$Mydata << EOD\n%s\nEOD' %(content))
    c = plot_cmd
    for cmd in args:
        c += ' $Mydata %s,' %(cmd)
    #print(c)
    g.cmd(c.rstrip(','))
    g.reset()

class Gnuplot(gnuplot.Gnuplot):
    """Unsophisticated interface to a running gnuplot program.

    See gp_unix.py for usage information.

    """

    def plot(self, *items, **kwargs):
        for k,v in kwargs.items():
            #print('set %s %s' %(k, v))
            self.set(**kwargs)

        c = 'plot'
        for item in items:
            c = c + " " + item + ","
        cmd = c.rstrip(',')
        self.__call__(cmd + '\n')

    def splot(self, *items):
        c = 'splot'
        for item in items:
            c = c + " " + item + ","
        cmd = c.rstrip(',')
        self.__call__(cmd + '\n')

if __name__ == '__main__':
    g = Gnuplot()
    #ts = pd.Series(np.random.randn(10))
