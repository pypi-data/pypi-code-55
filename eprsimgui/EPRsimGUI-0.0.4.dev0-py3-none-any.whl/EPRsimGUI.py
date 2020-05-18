#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 17:09:14 2019

@author: stephan
"""


import EPRsim.Nucdic as Nucdic
import sys
import os
import matplotlib
try:
    import EPRsimGUI
except ImportError:
    pass

try:
    from EPRsimGUI.Figure_handler import (figure_handler_init, figure_handler,
                                figure_handler_fit)
    import EPRsimGUI.SimGUI_functions as funcs
    from EPRsimGUI.Signals_slots import Signal_slots
    from EPRsimGUI.SimGUI_Design import Ui_SimGUIWindow
    from EPRsimGUI.PSE_Design import Ui_Dialog
except ImportError:
    from Figure_handler import (figure_handler_init, figure_handler,
                                       figure_handler_fit)
    import SimGUI_functions as funcs
    from Signals_slots import Signal_slots
    from SimGUI_Design import Ui_SimGUIWindow
    from PSE_Design import Ui_Dialog

from PyQt5.QtWidgets import (QApplication, QMainWindow, QDialog)
from PyQt5 import QtCore

# Define backend string for matplotlib
matplotlib.use("Qt5Agg", force=True)


# Subclass for printing in GUI instead of the console
class EmittingStream(QtCore.QObject):
    textWritten = QtCore.pyqtSignal(str)

    def write(self, text):
        self.textWritten.emit(str(text))

    def flush(self):
        pass


# Relative path (redirected in binary to _MEIPASS)
def resource_path(relative_path):
    try:
        try:
            return os.path.join(sys._MEIPASS, relative_path)
        except Exception:
            return os.path.join(EPRsimGUI.__path__[0], relative_path)
    except:
        return relative_path

# GUI Main class
class SimMainGuiDesign(QMainWindow, Ui_SimGUIWindow,
                          EmittingStream):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        funcs.initialize(self)
        sys.stdout = EmittingStream(textWritten=self.normalOutputWritten)
        print("Simulation GUI is active")
        # Define matplotlib for window  containered in QWidget
        figure_handler_init(self)
        Signal_slots(self)
        self.tablist = [self.Nuc_isotope, self.Nuc_isotope_2,
                        self.Nuc_isotope_3, self.Nuc_isotope_4]
        self.run_simulation()

    def normalOutputWritten(self, text):
        # Append text to the QTextEdit
        self.cursor = self.plainTextEdit.textCursor()
        self.cursor.insertText(text)
        self.plainTextEdit.setTextCursor(self.cursor)
        self.plainTextEdit.ensureCursorVisible()

    def next_stack(self):
        index = self.stackedWidget.currentIndex()
        self.stackedWidget.setCurrentIndex(index+1)

    def previous_stack(self):
        index = self.stackedWidget.currentIndex()
        self.stackedWidget.setCurrentIndex(index-1)

    def next_stack_exp(self):
        index = self.stackedWidget_exp.currentIndex()
        self.stackedWidget_exp.setCurrentIndex(index+1)

    def spinpolarization(self):
        funcs.process_spinpolarization(self)

    def previous_stack_exp(self):
        index = self.stackedWidget_exp.currentIndex()
        self.stackedWidget_exp.setCurrentIndex(index-1)

    def open_PSE(self):
        indx = self.stackedWidget.currentIndex()
        self.tablist[indx].clear()
        self.dialogPSE = QDialog()
        self.dialogPSE.ui = Ui_Dialog()
        self.dialogPSE.ui.setupUi(self.dialogPSE)
        self.dialogPSE.ui.Choose_element.accepted.connect(self.print_element)
        self.dialogPSE.show()

    def run_simulation(self):
        self.B, self.spc, self.Param, self.objective = funcs.simulation(self)
        self.update_figure()

    def reset_to_raw(self):
        funcs.reset_to_raw(self)

    def do_processing(self):
        if self.Exp_B is None:
            return
        else:
            funcs.post_processing_exp(self)
            self.update_figure()

    def update_figure(self):
        try:
            if self.Exp_B is None and self.B is not None:
                figure_handler(self, self.B, self.spc, False)
            elif self.Exp_B is not None and not self.show_simulation.isChecked():
                if self.show_imaginary.isChecked():
                    x = (self.Exp_B, self.Exp_B)
                    y = (self.Exp_spc, self.Exp_spc_imag)
                    figure_handler(self, x, y, True)
                else:
                    if self.MaintabWidget.currentIndex() == 1:
                        x = self.Exp_B
                        y = self.Exp_spc
                    else:
                        x = self.B
                        y = self.spc
                    figure_handler(self, x, y, False)
            else:
                figure_handler_fit(self, self.B, self.spc, self.Exp_B,
                                   self.Exp_spc, multi=False)
        except:
            print("Error by plotting data.")
        return

    def save(self):
        funcs.save_file(self)

    def load(self):
        funcs.open_files(self)

    def clear(self):
        funcs.clear_experiment(self)

    def print_element(self):
        indx = self.stackedWidget.currentIndex()
        row = self.dialogPSE.ui.PSE.currentRow()
        column = self.dialogPSE.ui.PSE.currentColumn()
        element = str(self.dialogPSE.ui.PSE.item(row, column).text())
        try:
            isotopes = Nucdic.isotopes_catalogue(element)
            isotopes.append(element)
            self.tablist[indx].addItems(isotopes)
        except KeyError:
            print("No stable isotope for this element")

"""********************************************************************
       MAIN GUI (EVENT) LOOP
********************************************************************"""

def run():
    # Main GUI Application
    app = QApplication(sys.argv)
    mainfun = SimMainGuiDesign()
    app.processEvents()
    mainfun.show()
    sys.exit(app.exec_())   

if __name__ == '__main__':
    # Main GUI Application
    app = QApplication(sys.argv)
    mainfun = SimMainGuiDesign()
    app.processEvents()
    mainfun.show()
    sys.exit(app.exec_())
     