#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 16:47:38 2019

@author: stephan
"""

import numpy as np
import os
import EPRsim.Tools as tool
import EPRsim.EPRsim as sim
try:
    from EPRsimGUI.Warning_Diag1 import Ui_Warning_Diag1
except ImportError:
    from Warning_Diag1 import Ui_Warning_Diag1
from PyQt5.QtWidgets import QDialog,  QFileDialog, QMessageBox
import datetime
from scipy import signal
from copy import copy
import xml.etree.ElementTree as ET
import base64


def initialize(self):
    self.fonts = 8
    self.tracecolor = "red"
    self.tracecolor_fit = "yellow"
    self.axiscolor = "white"
    self.backgroundcolor = "black"
    self.B, self.spc, self.Param = None, None, None
    self.Exp_B, self.Exp_spc, self.Exp_spc_imag = None, None, None
    self.Exp_spc_r, self.Exp_spc_imag_r = None, None
    self.objective = None
    return


def simulation(self):
    self.plainTextEdit.clear()
    Param = sim.Parameters()
    Param.g, Param.gFrame = define_g_tensor(self)
    Param.Range = define_field_range(self)
    Param.mwFreq = define_mwFreq(self)
    Param.lw = define_linewidth(self)
    Param.motion = define_motion(self, Param)
    Param.Harmonic = define_Harmonic(self)
    Param.tcorr = define_rotational_correlation_time(self)
    Param.Nucs, Param.A, Param.AFrame, Param.n = define_hyperfine(self)
    Param.D, Param.DFrame = define_D_tensor(self)
    Param.S = define_electron_spin(self)
    Param.mwPhase = define_Phase(self)
    Param.ModAmp = define_modulation_amplitude(self)
    Param.Points = define_points(self)
    Population = define_polarization(self)
    if Population is not None:
        Param.Population = Population
    objective = None
    try:
        field, spc, warning = sim.simulate([Param])
        if warning == 1:
            show_warning(self)
        spc = post_processing(self, field, spc, Param.Harmonic)
        if self.Exp_spc is not None:
            self.Exp_spc = post_processing(self, field, self.Exp_spc,
                                           Param.Harmonic)
            try:
                objective = objective_function(self.Exp_spc, spc)
            except ValueError:
                objective = None
    except:
        m = "An error occured during simulation. Please check your parameters!"
        print(m)
        field = np.linspace(Param.Range[0], Param.Range[1], int(Param.Points))
        spc = np.zeros(int(Param.Points))
    return field, spc, Param, objective


def clear_experiment(self):
    self.lineEditexpdata.setText("")
    self.Exp_B, self.Exp_spc = None, None
    self.objective = None
    self.run_simulation()


def objective_function(spc_exp, spc):
    try:
        obj = np.sum((spc_exp-spc)**2)
    except ValueError:
        obj = 0
    return obj


def show_warning(self):
    self.dialogwarning1 = QDialog()
    self.dialogwarning1.ui = Ui_Warning_Diag1()
    self.dialogwarning1.ui.setupUi(self.dialogwarning1)
    self.dialogwarning1.ui.pushButton.clicked.connect(lambda: reject(self))
    self.dialogwarning1.show()
    return


def reject(self):
    self.dialogwarning1.close()
    return


def post_processing(self,  field, spc, Harmonic):
    if self.norm_area.isChecked():
        spc = len(spc)*tool.normalize2area(spc, Harmonic)
    else:
        spc = spc/max(abs(spc)+1e-18)
    spc = modulate_or_integrate(self, spc, field)
    SNR = define_SNR(self)
    if SNR is not None:
        spc = tool.add_noise(spc, SNR)
    return spc


def modulate_or_integrate(self, spc, field):
    if self.Harmonic.value() == 2:
        spc = tool.pseudo_field_modulation(0.001, field, spc)
    elif self.Harmonic.value() == -1:
        spc = np.cumsum(spc)
    return spc

# *****************************************************************************
# DEFINE SIMULATION PARAMETERS
# *****************************************************************************


def set_lists(self):
    tab_ind = [self.tab_Nuc1.currentIndex(), self.tab_Nuc2.currentIndex(),
               self.tab_Nuc3.currentIndex(), self.tab_Nuc4.currentIndex()]
    check_ind = [self.Nuc1_checkbox.isChecked(),
                 self.Nuc2_checkbox.isChecked(),
                 self.Nuc3_checkbox.isChecked(),
                 self.Nuc4_checkbox.isChecked()]
    Aiso = [self.A_iso_box.value(),
            self.A_iso_box_2.value(),
            self.A_iso_box_3.value(),
            self.A_iso_box_4.value()]
    Apara = [self.A_ax_para_box.value(), self.A_ax_para_box_2.value(),
             self.A_ax_para_box_3.value(), self.A_ax_para_box_4.value()]
    Aper = [self.A_ax_perp_box.value(), self.A_ax_perp_box_2.value(),
            self.A_ax_perp_box_3.value(), self.A_ax_perp_box_4.value()]
    AperFrame = [self.A_perp_Frame.value(), self.A_perp_Frame_2.value(),
                 self.A_perp_Frame_3.value(), self.A_perp_Frame_4.value()]
    AparaFrame = [self.A_para_Frame.value(), self.A_para_Frame_2.value(),
                  self.A_para_Frame_3.value(), self.A_para_Frame_4.value()]
    Ax = [self.Ax_box.value(), self.Ax_box_2.value(),
          self.Ax_box_3.value(), self.Ax_box_4.value()]
    Ay = [self.Ay_box.value(), self.Ay_box_2.value(),
          self.Ay_box_3.value(), self.Ay_box_4.value()]
    Az = [self.Az_box.value(), self.Az_box_2.value(),
          self.Az_box_3.value(), self.Az_box_4.value()]
    AxFrame = [self.Ax_Frame.value(), self.Ax_Frame_2.value(),
               self.Ax_Frame_3.value(), self.Ax_Frame_4.value()]
    AyFrame = [self.Ay_Frame.value(), self.Ay_Frame_2.value(),
               self.Ay_Frame_3.value(), self.Ay_Frame_4.value()]
    AzFrame = [self.Az_Frame.value(), self.Az_Frame_2.value(),
               self.Az_Frame_3.value(), self.Az_Frame_4.value()]
    n = [self.N_eqiuv.value(), self.N_eqiuv_2.value(),
         self.N_eqiuv_3.value(), self.N_eqiuv_4.value()]
    Nuc = [str(self.Nuc_isotope.currentText()),
           str(self.Nuc_isotope_2.currentText()),
           str(self.Nuc_isotope_3.currentText()),
           str(self.Nuc_isotope_4.currentText())]
    return (tab_ind, check_ind, Aiso, Apara, Aper, AperFrame, AparaFrame,
            Ax, Ay, Az, AxFrame, AyFrame, AzFrame, Nuc, n)


def define_hyperfine(self):
    (tab_ind, check_ind, Aiso, Apara, Aper, AperFrame, AparaFrame, Ax, Ay, Az,
     AxFrame, AyFrame, AzFrame, Nuc, n) = set_lists(self)
    A_r = None
    AFrame_r = None
    Nuc_r = None
    n_r = None
    k = 0
    for i in range(0, 4):
        if check_ind[i]:
            if Nuc[i] == "":
                continue
            if tab_ind[i] == 0:
                A = [Aiso[i], Aiso[i], Aiso[i]]
                AFrame = [0, 0, 0]
            elif tab_ind[i] == 1:
                A = [Aper[i], Aper[i], Apara[i]]
                AFrame = [AperFrame[i], AperFrame[i], AparaFrame[i]]
            else:
                A = [Ax[i], Ay[i], Az[i]]
                AFrame = [AxFrame[i], AyFrame[i], AzFrame[i]]
            if A_r is not None:
                if k == 1:
                    A_r = [A_r]
                    AFrame_r = [AFrame_r]
                    n_r = [n_r]
                A_r.append(A)
                AFrame_r.append(tool.degree_in_rad(np.asarray(AFrame)))
                Nuc_r += ","+Nuc[i]
                n_r.append(int(n[i]))
            else:
                A_r = A
                AFrame_r = tool.degree_in_rad(np.asarray(AFrame))
                Nuc_r = Nuc[i]
                n_r = int(n[i])
            k += 1
    return Nuc_r, A_r, AFrame_r, n_r


def define_g_tensor(self):
    if self.tab_g.currentIndex() == 0:
        giso = self.g_iso_box.value()
        g = [giso, giso, giso]
        Frame = [0, 0, 0]
    elif self.tab_g.currentIndex() == 1:
        gperp = self.g_ax_perp_box.value()
        gperpFrame = self.g_perp_Frame.value()
        gpara = self.g_ax_para_box.value()
        gparaFrame = self.g_ax_para_box.value()
        g = [gperp, gperp, gpara]
        Frame = [gperpFrame, gperpFrame, gparaFrame]
    else:
        gx = self.gx_box.value()
        gy = self.gy_box.value()
        gz = self.gz_box.value()
        gxFrame = self.gx_Frame.value()
        gyFrame = self.gy_Frame.value()
        gzFrame = self.gz_Frame.value()
        g = [gx, gy, gz]
        Frame = [gxFrame, gyFrame, gzFrame]
    Frame = tool.degree_in_rad(np.asarray(Frame))
    return g, Frame


def define_Harmonic(self):
    Harmonic = self.Harmonic.value()
    if Harmonic == 2:
        Harmonic = 1
    elif Harmonic == -1:
        Harmonic = 0
    return int(Harmonic)


def define_electron_spin(self):
    S = self.Electron_spin.value()
    S = round(S*2)/2
    self.Electron_spin.setValue(S)
    return S


def define_mwFreq(self):
    mwfreq = self.mwFreq.value()
    return mwfreq


def define_field_range(self):
    rmax = self.Field_max.value()
    rmin = self.Field_min.value()
    Range = [rmin, rmax]
    if Range[0] > Range[1]:
        Range = [Range[1], Range[0]]
    return Range


def define_linewidth(self):
    gauss = self.lw_Gauss.value()
    lorenz = self.lw_Lorentz.value()
    lw = [gauss, lorenz]
    if lw[0] < 0.0025:
        lw[0] = 0.0025
    return lw


def define_rotational_correlation_time(self):
    if self.checkBox_fast.isChecked():
        logtcorr = self.logtcorr.value()
        tcorr = np.power(10.0, logtcorr)
    else:
        tcorr = None
    return tcorr


def define_D_tensor(self):
    D = self.D_value.value()
    E = self.E_value.value()
    D = [D, E]
    DFrame = [self.Dx_Frame.value(), self.Dy_Frame.value(),
              self.Dz_Frame.value()]
    DFrame = tool.degree_in_rad(np.asarray(DFrame))
    return D, DFrame


def define_Phase(self):
    phase = tool.degree_in_rad(self.mwPhase.value())
    return phase


def define_motion(self, Param):
    if self.checkBox_solid.isChecked():
        motion = 'solid'
    else:
        motion = 'fast'
    return motion


def define_modulation_amplitude(self):
    modamp = self.modAmp.value()
    return modamp


def define_SNR(self):
    if self.Use_noise.isChecked():
        SNR = self.SNR.value()
    else:
        SNR = None
    return SNR


def define_polarization(self):
    Pol = None
    if self.Use_spin_polarization.isChecked():
        P0, P1, P2 = self.P0.value(), self.P1.value(), self.P2.value()
        if self.Electron_spin.value() == 1.0:
            Pol = [P0, P1, P2]
        elif self.Electron_spin.value() == 1.5:
            Pol = [P0, P1, P2, self.P3.value()]
        elif self.Electron_spin.value() == 2.0:
            Pol = [P0, P1, P2, self.P3.value(), self.P4.value()]
    return Pol


def define_points(self):
    points = int(self.nPoints.value())
    return points

# *****************************************************************************
# HANDLE SPIN POLARIZATION
# *****************************************************************************


def process_spinpolarization(self):
    if self.Electron_spin.value() < 1.0:
        disable_spin_polarization(self)
    elif self.Electron_spin.value() == 1.0:
        set_triplet_pol(self)
    elif self.Electron_spin.value() == 1.5:
        set_quart_pol(self)
    elif self.Electron_spin.value() == 2.0:
        set_quint_pol(self)
    else:
        disable_spin_polarization(self)
    return


def set_quint_pol(self):
    tmpstr1 = ("background-color: "+"rgb(255, 255, 255);")
    self.P0.setStyleSheet(tmpstr1)
    self.P0.setReadOnly(False)
    self.P1.setStyleSheet(tmpstr1)
    self.P1.setReadOnly(False)
    self.P2.setStyleSheet(tmpstr1)
    self.P2.setReadOnly(False)
    self.P3.setStyleSheet(tmpstr1)
    self.P3.setReadOnly(False)
    self.P4.setStyleSheet(tmpstr1)
    self.P4.setReadOnly(False)


def set_quart_pol(self):
    tmpstr = ("background-color: "+"rgb(117, 117, 117);")
    tmpstr1 = ("background-color: "+"rgb(255, 255, 255);")
    self.P0.setStyleSheet(tmpstr1)
    self.P0.setReadOnly(False)
    self.P1.setStyleSheet(tmpstr1)
    self.P1.setReadOnly(False)
    self.P2.setStyleSheet(tmpstr1)
    self.P2.setReadOnly(False)
    self.P3.setStyleSheet(tmpstr1)
    self.P3.setReadOnly(False)
    self.P4.setStyleSheet(tmpstr)
    self.P4.setReadOnly(True)


def set_triplet_pol(self):
    tmpstr = ("background-color: "+"rgb(117, 117, 117);")
    tmpstr1 = ("background-color: "+"rgb(255, 255, 255);")
    self.P0.setStyleSheet(tmpstr1)
    self.P0.setReadOnly(False)
    self.P1.setStyleSheet(tmpstr1)
    self.P1.setReadOnly(False)
    self.P2.setStyleSheet(tmpstr1)
    self.P2.setReadOnly(False)
    self.P3.setStyleSheet(tmpstr)
    self.P3.setReadOnly(True)
    self.P4.setStyleSheet(tmpstr)
    self.P4.setReadOnly(True)


def disable_spin_polarization(self):
    tmpstr = ("background-color: "+"rgb(117, 117, 117);")
    self.Use_spin_polarization.setChecked(False)
    self.P0.setStyleSheet(tmpstr)
    self.P0.setReadOnly(True)
    self.P1.setStyleSheet(tmpstr)
    self.P1.setReadOnly(True)
    self.P2.setStyleSheet(tmpstr)
    self.P2.setReadOnly(True)
    self.P3.setStyleSheet(tmpstr)
    self.P3.setReadOnly(True)
    self.P4.setStyleSheet(tmpstr)
    self.P4.setReadOnly(True)


# *****************************************************************************
# EXPERIMENTAL DATA PROCESSING FUNCTIONS
# *****************************************************************************


def pseudomod(spc, field, modamp):
    spc = tool.pseudo_field_modulation(modamp, field, spc)
    return spc


def do_phase_offset(phase, spc, spc_imag=None):
    if spc_imag is None:
        spc_im = signal.hilbert(spc)
    else:
        spc_im = spc+1j*spc_imag
    spc_im = np.exp(-1j*phase)*spc_im
    return np.real(spc_im), np.imag(spc_im)


def do_baseline_function(degree, spc, field, full_field):
    x = np.polyfit(field, spc,  deg=degree)
    polyfun = np.polyval(x, full_field)
    return polyfun


def do_baseline_correction(spc, poly):
    spc -= poly
    return spc


def do_savgol_filtering(spc):
    spc = signal.savgol_filter(spc, 7, 3)
    return spc


def do_median_filtering(spc):
    spc = signal.medfilt(spc, kernel_size=5)
    return spc


def do_Gaussian_smoothing(self, field, spc):
    width = self.Gausssmoth_value.value()
    spc = tool.convolution_G(width, field, spc)
    return spc


def integrate(spc):
    spc = np.cumsum(spc)
    return spc


def reset_to_raw(self):
    self.Do_phase_correction.setChecked(False)
    self.Do_baseline_correction.setChecked(False)
    self.normalize_maxInt.setChecked(True)
    self.Do_smoothing.setChecked(False)
    self.Enable_integration.setChecked(False)
    self.Enable_pseudo_mod.setChecked(False)
    post_processing_exp(self)
    self.update_figure()


def post_processing_exp(self):
    """
    Processing hierachy:
        1: Phase correction
        2: Baseline correction
        3: Pseudo-modulation
        4: Integration
        5: Smoothing/Filtering
        6: Normalization
    """
    if self.Exp_spc_r is None:
        return
    self.Exp_spc = copy(self.Exp_spc_r)
    self.Exp_spc_imag = copy(self.Exp_spc_imag_r)
    if self.Do_phase_correction.isChecked():
        phase_angle = self.Phase_angle.value()
        phase_angle = tool.degree_in_rad(phase_angle)
        self.Exp_spc, self.Exp_spc_imag = do_phase_offset(phase_angle,
                                                          self.Exp_spc,
                                                          self.Exp_spc_imag)
    if self.Do_baseline_correction.isChecked():
        poly = self.Polynomial_degree.value()
        try:
            indices = np.where((self.Exp_B < self.Baseline_low.value()) |
                               (self.Exp_B > self.Baseline_up.value()))[0]
            field = self.Exp_B[indices]
            spc = self.Exp_spc[indices]
            polyfun = do_baseline_function(poly, spc, field, self.Exp_B)
            self.Exp_sp = do_baseline_correction(self.Exp_spc, polyfun)
        except TypeError:
            print("Some error occured. Please set proper boundaries.")
            self.Do_baseline_correction.setChecked(False)

    if self.Enable_pseudo_mod.isChecked():
        modamp = self.ModAmp_value.value()
        self.Exp_spc = pseudomod(self.Exp_spc, self.Exp_B, modamp)
        self.Exp_spc_imag = pseudomod(self.Exp_spc_imag, self.Exp_B, modamp)

    if self.Enable_integration.isChecked():
        self.Exp_spc = integrate(self.Exp_spc)
        self.Exp_spc_imag = integrate(self.Exp_spc_imag)
        if self.Second_integral.isChecked():
            self.Exp_spc = integrate(self.Exp_spc)
            self.Exp_spc_imag = integrate(self.Exp_spc_imag)

    if self.Do_smoothing.isChecked():
        if self.Savitzky_Golay.isChecked():
            self.Exp_spc = do_savgol_filtering(self.Exp_spc)
            self.Exp_spc_imag = do_savgol_filtering(self.Exp_spc_imag)
        elif self.Gaussian_smoothing.isChecked():
            self.Exp_spc = do_Gaussian_smoothing(self, self.Exp_B,
                                                 self.Exp_spc)
            self.Exp_spc_imag = do_Gaussian_smoothing(self, self.Exp_B,
                                                      self.Exp_spc_imag)
        elif self.Median_filter.isChecked():
            self.Exp_spc = do_median_filtering(self.Exp_spc)
            self.Exp_spc_imag = do_median_filtering(self.Exp_spc_imag)
    if self.normalize_area.isChecked():
        self.Exp_spc, self.Exp_spc_imag = normalization_exp(self.Exp_spc,
                                                            self.Exp_spc_imag,
                                                            True)
    else:
        self.Exp_spc, self.Exp_spc_imag = normalization_exp(self.Exp_spc,
                                                            self.Exp_spc_imag,
                                                            False)
    return


# *****************************************************************************
# OPEN AND SAVE FILES
# *****************************************************************************

def save_file(self):
    self.dialog = QFileDialog()
    self.dialog.setStyleSheet("background-color:rgb(0, 196, 255)")
    str_tmp = "*.txt (*.txt);;*dat (*.dat)"
    name, name_tmp = self.dialog.getSaveFileName(self, 'Save File', None,
                                                 str_tmp)
    if not name:
        return
    self.save_name = name
    self.save_name = str(self.save_name)
    if not (self.save_name.endswith('.txt') or
            self.save_name.endswith('.dat')):
        self.save_name += '.txt'
    filetyp = '.txt'
    if '.txt' in self.save_name:
        pos = self.save_name.index('.txt')
        filetyp = '.txt'
        self.save_name = self.save_name[0:pos]
    elif '.dat' in self.save_name:
        pos = self.save_name.index('.dat')
        filetyp = '.dat'
        self.save_name = self.save_name[0:pos]
    save_infosheet(self, filetyp)
    save_simulation(self, filetyp)
    return


def save_simulation(self, filetyp):
    y = np.asarray((self.B, self.spc))
    y = np.transpose(y)
    with open(self.save_name+"_simulation"+filetyp, 'w') as file:
        file.write("\n".join("   ".join(map("{:.8f}".format, x)) for x in (y)))
    return


def save_infosheet(self, filetyp):
    with open(self.save_name+"_infosheet"+filetyp, 'w') as file:
        file.write("\n")
        file.write("***************************************************\n")
        file.write("*           cw-EPR simulation package             *\n")
        file.write("*                                                 *\n")
        file.write("*     Stephan Rein, University of Freiburg        *\n")
        file.write("*                                                 *\n")
        file.write("*               Version 0.0.1                     *\n")
        file.write("***************************************************\n")
        file.write("\nInfosheet for:\n"+str(os.path.basename(self.save_name)) +
                   "\n\n")
        now = datetime.datetime.now()
        file.write("Date: "+now.strftime("%Y-%m-%d %H:%M:%S"))
        sortedkeys = sorted(self.Param.__dict__, key=str.lower)
        file.write("\n\nPARAMETERS:\n")
        for keys in sortedkeys:
            if not keys.startswith("_"):
                file.write(keys + ": " + str(self.Param.__dict__[keys]))
                file.write("\n")


def open_files(self):
    self.dialog = QFileDialog()
    str_tmp = ("*.txt (*.txt *.TXT);;*dat (*.dat .*DAT);;*DTA (*DTA *dta);;"+
               "*spc (*spc *SPC);;*xml (*xml *XML);;")
    name, name_tmp = self.dialog.getOpenFileName(self, 'Open File', None,
                                                 str_tmp)
    if not name:
        return
    try:
        if (name.endswith('.txt') or name.endswith('.TXT') or
           name.endswith('.dat') or name.endswith('.DAT')):
            loadtextfile(self, name)
        elif name.endswith('.DTA') or name.endswith('.dta'):
            loadDTAfile(self, name)
        elif name.endswith('.spc') or name.endswith('.SPC'):
            loadSPCfile(self, name)
        elif name.endswith('.xml') or name.endswith('.XML'):
            loadXML(self, name)
        extract_filename(self, name)
        self.lineEditexpdata.setText(str(self.filename))
        self.Exp_spc_r, self.Exp_spc_imag_r = do_phase_offset(0, self.Exp_spc)
        self.Exp_spc = copy(self.Exp_spc_r)
        self.Exp_spc_imag = copy(self.Exp_spc_imag_r)
        self.Field_min.setValue(min(self.Exp_B))
        self.Field_max.setValue(max(self.Exp_B))
        self.nPoints.setValue(len(self.Exp_B))
        self.objective = objective_function(self.Exp_spc, self.spc)
        print("\nFile was sucessfully loaded.")
        fieldlenght = np.max(self.Exp_B)-np.min(self.Exp_B)
        margin = fieldlenght/10.0
        self.Baseline_low.setValue(float(np.min(self.Exp_B)+margin))
        self.Baseline_up.setValue(float(np.max(self.Exp_B)-margin))
        post_processing_exp(self)
        #self.run_simulation()
        self.update_figure()
    except:
        self.error_dialog = QMessageBox()
        self.error_dialog.setWindowTitle("Import Error")
        self.error_dialog.setText("File could not be loaded!.")
        self.error_dialog.show()
        return


def loadXML(self, name):
    tree = ET.parse(name)
    data = []
    key = []
    attr = []
    for node in tree.findall('.//Data/Measurement/DataCurves/Curve'):
        key.append(node.tag)
        data.append(node.text)
        attr.append(node.attrib)
    B = np.empty(0)
    spc = np.empty(0)
    for i in range(0, len(key)):
        attr_tmp = attr[i]
        data_tmp = data[i]
        if attr_tmp["Name"] == "BField":
            data_tmp = data_tmp.split("=")
            dt = np.dtype(float)
            for elements in data_tmp:
                bytecode = base64.b64decode(elements + "==")
                B = np.append(B, np.frombuffer(bytecode, dtype=dt))
        if attr_tmp["Name"] == "MWAbsorption":
            dt = np.dtype(float)
            dt = dt.newbyteorder('<')
            data_tmp = data_tmp.split("=")
            for elements in data_tmp:
                bytecode = base64.b64decode(elements + "==")
                spc = np.append(spc, np.frombuffer(bytecode, dtype=dt))
    self.Exp_spc = spc
    self.Exp_B = np.linspace(min(B), max(B), len(self.Exp_spc))


def loadtextfile(self, name):
    Input = np.loadtxt(name)
    self.Exp_spc = Input[:, 1]
    self.Exp_B = Input[:, 0]
    return


def loadDTAfile(self, name):
    f = open(name, 'rb')
    data_type = np.dtype('>f8')
    Input = np.fromfile(f, data_type)
    Input = Input.astype(float)
    (self.Exp_spc, self.Exp_spc_imag,
     self.Exp_B) = read_input_var_DSC(Input, name)


def read_input_var_DSC(Input, filename=None):
    # Default setting for complex signal
    filename = filename[0:len(filename)-4]
    filename = filename+".DSC"
    f = open(filename, 'r')
    t = f.readlines()
    for l in t:
        if l.startswith('IKKF'):
            s = l.split()
            if s[1] == 'CPLX':
                complexsignal = True
            else:
                complexsignal = False
            continue
        if l.startswith('XPTS'):
            s = l.split()
            npoints = int(s[1])
            continue
        if l.startswith('XMIN'):
            s = l.split()
            start = float(s[1])
            continue
        if l.startswith('XWID'):
            s = l.split()
            width = float(s[1])
            continue
    if complexsignal:
        spc_imag = Input[1:len(Input):2]
        spc = Input[0:len(Input):2]
    elif not complexsignal:
        spc = Input
        spc_imag = None
    B = np.linspace(start, start+width, npoints)
    # Convert to mT
    B = B/10.0
    return spc, spc_imag, B


def loadSPCfile(self, name):
    f = open(name, 'rb')
    data_type = np.dtype('<f4')
    Input = np.fromfile(f, data_type)
    self.Exp_spc = Input.astype(float)
    self.Exp_spc_imag = None
    self.Exp_B = read_input_var_PAR(Input, name)


def read_input_var_PAR(Input, filename=None):
    # Default setting for complex signal
    filename = filename[0:len(filename)-4]
    filename = filename+".par"
    try:
        f = open(filename, 'r')
    except:
        filename = filename[0:len(filename)-4]
        filename = filename+".PAR"
        f = open(filename, 'r')
    t = f.readlines()
    for l in t:
        if l.startswith('ANZ'):
            s = l.split()
            npoints = int(s[1])
            continue
        if l.startswith('HCF'):
            s = l.split()
            center = float(s[1])
            continue
        if l.startswith('HSW'):
            s = l.split()
            width = float(s[1])
            continue
    B = np.linspace(center-width/2, center+width/2, npoints)
    # Convert to mT
    B = B/10.0
    return B


def normalization_exp(real, imag, area=False):
    if not area:
        normfac = max(abs(real))
    else:
        normfac = len(real)*np.sum(np.absolute(real))
    real = real/normfac
    imag = imag/normfac
    return real, imag


def extract_filename(self, name):
    # Give information about the filename
    ind = name.rfind("/")
    if ind == -1:
        self.filename = name
    else:
        self.filename = name[ind+1:]
    return
