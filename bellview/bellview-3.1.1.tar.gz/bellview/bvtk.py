######################################################################
### Bell View
### Copyright (c) 2020 Jonathan Wilson
### Please refer to help/licence.txt for further information
### File: bvtk.py
### Description: Load Tk modules, dependent on Python version
### Last Modified: 24 May 2020
######################################################################

from sys import version_info

if version_info[0]==2:
    from Tkinter import *
    from ttk import *
    from tkFileDialog import askopenfilename, asksaveasfilename, askopenfilenames
    from tkColorChooser import askcolor
    from tkMessageBox import askyesno, showinfo, showerror

elif version_info[0]==3:
    from tkinter import *
    from tkinter.ttk import *
    from tkinter.filedialog import askopenfilename, asksaveasfilename, askopenfilenames
    from tkinter.colorchooser import askcolor
    from tkinter.messagebox import askyesno, showinfo, showerror

else:
    raise Exception('Unsupported version of Python')

