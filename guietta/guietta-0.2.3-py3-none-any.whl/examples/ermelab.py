# -*- coding: utf-8 -*-

import os
from guietta import Gui, LB, _, III, M

basedir = '/home/alfio/guietta'

def days(gui, text):
    gui.tn = os.listdir(os.path.join(basedir, text))

def tn(gui, tn):
    print(tn)

def psd(gui, *args):
    pass

gui = Gui(
    
  [ LB('days'),  LB('tn')  ,  M('Modalplot') ],
  [     III   ,    III     ,  ['PSD']        ],
  [     III   ,    III     ,    _            ],
)

gui.events(
    
  [   days    ,     tn     ,     _           ],
  [     _     ,     _      ,     psd         ],
  [     _     ,     _      ,     _           ],
   )

#from PyQt5.QtWidgets import  QAbstractItemView
#gui.widgets['tn'].setSelectionMode(QAbstractItemView.ExtendedSelection)

gui.days = os.listdir(basedir)

gui.run()

    