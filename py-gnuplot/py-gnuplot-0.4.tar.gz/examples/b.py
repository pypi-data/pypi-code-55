#!/usr/bin/env python
#coding=utf8

import sys, string, types
#sys.path.insert(0, '../gnuplotpy')
import gnuplotpy

if __name__ == '__main__':
    g = gnuplotpy.Gnuplot()
    g.set(term = 'pngcairo size 900,600', output = '"b.png"')

    g['multiplot'] = 'layout 2, 2 title "Derivatives of Sin(x)" font "Times-Roman, 22"'
    g.set('xmtics',
            title = '"各城市月平均降水量"',
            xlabel = '"月份"',
            ylabel = '"降水量（毫米）"',
            y2label = '"Error Magnitude" font "Courier, 12"',
            xrange = '[0.5:12.5]',
            xtics = 'border in 1,1,12 add ("Pi" 3.14159)',
            mxtics = '10',
            ytics = 'nomirror',
            y2tics = '0,25,150',
            label = '"Approximation error" right at 5,270 offset -1,1',
            key = 'title "Legend" nobox',
            grid = "y2tics")
    g['arrow 1'] = 'from first 4.5, 270 to 5,172 lt 1 lw 2 front size .3,15'
    g.plot('"b.dat" using 1:2 w lp pt 5 title "ShangHai"',
            '"b.dat" using 1:3 w lp pt 7 title "Beijing"',
            '100 * sin(x) title "100*sin(x)"')
    g.unset('title', 'xlabel', 'ylabel', 'y2label', 'xrange', 'mxtics', 'xmtics')

    g['title'] = '"besj1(x)"'
    g.plot('besj1(x)')
    g.plot('besy0(x)')
    g.plot('besy1(x)')
    g.reset()

    g('pause mouse')

