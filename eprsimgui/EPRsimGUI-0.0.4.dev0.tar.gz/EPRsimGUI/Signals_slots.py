#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 10:44:20 2019

@author: stephan
"""


def Signal_slots(self):
    self.nextbutton.clicked.connect(self.next_stack)
    self.nextbutton_2.clicked.connect(self.next_stack)
    self.nextbutton_3.clicked.connect(self.next_stack)
    self.nextbutton_5.clicked.connect(self.next_stack_exp)
    self.previous_button.clicked.connect(self.previous_stack)
    self.previous_button_2.clicked.connect(self.previous_stack)
    self.previous_button_3.clicked.connect(self.previous_stack)
    self.previous_button_5.clicked.connect(self.previous_stack_exp)
    self.find_nuc_button.clicked.connect(self.open_PSE)
    self.find_nuc_button_2.clicked.connect(self.open_PSE)
    self.find_nuc_button_3.clicked.connect(self.open_PSE)
    self.find_nuc_button_4.clicked.connect(self.open_PSE)
    self.Start_simulation_button.clicked.connect(self.run_simulation)
    self.Save_button.clicked.connect(self.save)
    self.Loadbutton.clicked.connect(self.load)
    self.Clear_Exp_button.clicked.connect(self.clear)
    self.show_realpart.stateChanged.connect(self.update_figure)
    self.show_simulation.stateChanged.connect(self.update_figure)
    self.Do_processing.clicked.connect(self.do_processing)
    self.show_imaginary.stateChanged.connect(self.update_figure)
    self.MaintabWidget.currentChanged.connect(self.update_figure)
    self.Reset_processing.clicked.connect(self.reset_to_raw)
    self.Use_spin_polarization.stateChanged.connect(self.spinpolarization)
    self.Electron_spin.valueChanged.connect(self.spinpolarization)
    return
