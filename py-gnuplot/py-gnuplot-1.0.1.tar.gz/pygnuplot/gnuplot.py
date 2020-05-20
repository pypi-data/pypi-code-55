#!/usr/bin/env python
#coding=utf8
"""
Gnuplot for python
"""

import sys, string, types
import collections
import subprocess
try:
    # Python 2.
    from StringIO import StringIO
    # Python 3.
except ImportError:
    from io import StringIO
#import numpy as np  
#import pandas as pd

def make_subplot(*args, **kwargs):
    subplot = {'cmd': []}
    subplot["attribute"] = collections.OrderedDict()

    for v in args:
        subplot["cmd"].append(v)
    for k,v in kwargs.items():
        subplot["attribute"][k] = v
    return subplot

def multiplot(*args, **kwargs):
    '''
    @args: the subplot object list;
    @kwargs: the setting options that need to be set before call plot;
    '''
    g = gnuplot.Gnuplot()

    for k,v in kwargs.items():
        #print('set %s %s' %(k, v))
        g.cmd('set %s %s' %(k, v))
        #g.set(**kwargs)

    #print(args)
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
        c = 'plot '
        for cmd in subplot["cmd"]:
            c += '$Mydata %s, ' %(cmd)
        #print(c)
        g.cmd(c)
        # multiplot automatically unset all the label after one subplot.
        g.cmd('unset for [i=1:200] label i')
    g.reset()

def plot(*args, **kwargs):
    __gnuplot("plot", *args, **kwargs)

def splot(*args, **kwargs):
    __gnuplot("splot", *args, **kwargs)

def __gnuplot(plot_cmd, *args, **kwargs):
    g = Gnuplot()

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

    c = plot_cmd
    for cmd in args:
        c += ' %s,' %(cmd)
    #print(c.rstrip(','))
    g.cmd(c.rstrip(','))
    g.reset()

class Gnuplot(object):
    """Unsophisticated interface to a running gnuplot program.

    See gp_unix.py for usage information.

    """

    def __init__(self, *args, **kwargs):
        '''
        attributes and kwargs are non-ordered, if there is order requirement,
        please call set many times in order after init.
        '''
        self.gnuplot = subprocess.Popen(['gnuplot','-p'], shell=True, stdin=subprocess.PIPE)
        # forward write and flush methods:
        self.write = self.gnuplot.stdin.write
        self.flush = self.gnuplot.stdin.flush

        for v in args:
            #print v
            self.__call__('set %s' %(v))
        # kwargs input:
        for k,v in kwargs.items():
            self[k] = v
            #print ('set %s %s' %(k, v))
            self.__call__('set %s %s' %(k, v))

    def __del__(self):
        self.close()

    def cmd(self, *args):
        commands = []
        for cmd in args:
            #print StringIO(cmd.strip()).readlines()
            cmd = filter(lambda x: (x.strip()) and (x.strip()[0] != '#'),
                    StringIO(cmd.strip()).readlines())
            # remove the leading or trailing \r\n
            commands += map(lambda x: x.strip(), cmd)

        for c in commands:
            #print('%s' %(c))
            self.__call__('%s' %(c))

    def close(self):
        if self.gnuplot is not None:
            self.gnuplot.stdin.write(bytes('quit\n', encoding = "utf8")) #close the gnuplot window
            self.gnuplot = None

    def abort(self):
        if self.gnuplot is not None:
            self.gnuplot.kill()
            self.gnuplot = None

    def cd(self, path):
        self.__call__('cd %s' %(path))

    def call(self, filename, *items):
        params = ""
        for item in items:
            params += " " + item
        self.__call__('call "%s" %s' %(filename, params))

    def clear(self):
        self.__call__('clear')

    def do(self, iteration, *commands):
        self.__call__('do %s {' %(iteration))
        for cmd in commands:
            self.__call__('%s' %(cmd))
        self.__call__('}')

    def set(self, *args, **kwargs):
        '''
        kwargs is non-ordered, if there is order requirement, please call set
        many times in order.
        '''
        for v in args:
            #print('set %s' %(v))
            self.__call__('set %s' %(v))
        for k, v in kwargs.items():
            #print('set %s %s' %(k, v))
            self.__call__('set %s %s' %(k, v))

    def unset(self, *items):
        for item in items:
            self.__call__('unset %s\n' %(item))

    def reset(self):
        self.__call__('reset')

    def plot(self, *items, **kwargs):
        for k,v in kwargs.items():
            #print('set %s %s' %(k, v))
            self.set(**kwargs)

        c = 'plot'
        for item in items:
            c = c + " " + item + ","
        cmd = c.rstrip(',')
        self.__call__(cmd + '\n')

    # print function couldn't be compiled.
    #def print(self, *items):
    #    c = 'print'
    #    for item in items:
    #        c = c + " " + item + ","
    #    cmd = c.rstrip(',')
    #    self.__call__(cmd + '\n')

    def splot(self, *items):
        c = 'splot'
        for item in items:
            c = c + " " + item + ","
        cmd = c.rstrip(',')
        self.__call__(cmd + '\n')


    def evaluate(self, cmd):
        self.__call__('evaluate %s' %(cmd))

    def exit(self):
        self.__call__('exit')

    def fit(self, cmd):
        #TODO: to be done.
        self.__call__('fit %s' %(cmd))

    def help(self, cmd):
        self.__call__('help %s\r\n' %(cmd))

    def history(self, cmd):
        self.__call__('history %s' %(cmd))

    def load(self, filename):
        self.__call__('load %s' %(cmd))

    def pause(self, param):
        self.__call__('pause %s\n' %(param))

    def __getitem__(self, name): return self.__dict__.get(name.lower(), None)

    def __setitem__(self, name, value):
        #print name,value
        self.__call__('set %s %s\n' %(name, value))

    def __call__(self, s):
        """Send a command string to gnuplot, followed by newline."""
        cmd = s + '\n'
        self.write(cmd.encode('utf-8'))
        self.flush()

if __name__ == '__main__':
    g = Gnuplot()
    #ts = pd.Series(np.random.randn(10))
