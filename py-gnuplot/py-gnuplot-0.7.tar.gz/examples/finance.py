#!/usr/bin/env python
#coding=utf8

import sys, string, types
sys.path.insert(0, '../gnuplotpy')
import gnuplotpy
import collections
import json

if __name__ == '__main__':
    attributes = {
            'term': 'png size 900,600',
            'output': '"finance.png"',
            'lmargin': '9',
            'rmargin': '2',
            'format': 'x',
            'logscale': 'y',
            'xtics': '(66, 87, 109, 130, 151, 174, 193, 215, 235)',
            'ytics': '(105, 100, 95, 90, 85, 80)',
            'xrange': '[50:253]',
            'yrange': '[75:105]',
            'ylabel': '"price" offset 1',
            'label 1': '"Acme Widgets" at graph 0.5, graph 0.9 center front',
            'label 2': '"Courtesy of Bollinger Capital" at graph 0.01, 0.07',
            'label 3': '"  www.BollingerBands.com" at graph 0.01, 0.03',
            }
    g = gnuplotpy.Gnuplot(attributes)

    # figure 1
    g.set('grid', 'multiplot',
            title = '"Change to candlesticks"',
            size = '1, 0.7',
            origin = '0, 0.3',
            bmargin = '0')
    g.plot('"finance.dat" using 0:2:3:4:5 notitle with candlesticks lt 8',
            '"finance.dat" using 0:9 notitle with lines lt 3',
            '"finance.dat" using 0:10 notitle with lines lt 1',
            '"finance.dat" using 0:11 notitle with lines lt 2',
            '"finance.dat" using 0:8 axes x1y2 notitle with lines lt 4')
    g.unset('label 1', 'label 2', 'label 3', 'title', 'logscale y')

    # figure 2
    g.set('bmargin', 'format x',
            size = '1, 0.3',
            origin = '0.0, 0.0',
            autoscale = 'y',
            tmargin = '0',
            format = 'y "%1.0f"',
            xtics = '("6/03" 66, "7/03" 87, "8/03" 109, "9/03" 130, "10/03" 151, "11/03" 174, "12/03" 193, "1/04" 215, "2/04" 235)',
            ytics = '500',
            ylabel = '"volume (0000)" offset 1')
    g.plot('"finance.dat" using 0:($6/10000) notitle with impulses lt 3',
            '"finance.dat" using 0:($7/10000) notitle with lines lt 1')
    g.unset('multiplot')
    g.pause('3')
