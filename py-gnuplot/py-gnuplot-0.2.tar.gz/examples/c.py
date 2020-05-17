#!/usr/bin/env python
#coding=utf8

import sys, string, types
sys.path.insert(0, '../gnuplotpy')
import gnuplotpy

if __name__ == '__main__':
    g = gnuplotpy.Gnuplot()
    g.set(term = 'pngcairo size 900,600', output = '"c.png"')
    g.set(multiplot = 'layout 2,2')

#    do for [name in "A B C D"] {
#        filename = name . ".dat"
#        set title sprintf("Condition %s",name)
#        plot filename title name
#    }
    g.do('for [name in "a b c d"]',
        'filename = name . ".dat"',
        'set title sprintf("Condition %s",name)',
        'plot filename title name')

    g.unset('multiplot')

