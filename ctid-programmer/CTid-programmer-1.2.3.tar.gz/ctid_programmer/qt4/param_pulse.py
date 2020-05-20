# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ctid_programmer/qt4/param_pulse.ui'
#
# Created by: PyQt4 UI code generator 4.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Param_Pulse(object):
    def setupUi(self, Param_Pulse):
        Param_Pulse.setObjectName(_fromUtf8("Param_Pulse"))
        Param_Pulse.resize(343, 161)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Param_Pulse.sizePolicy().hasHeightForWidth())
        Param_Pulse.setSizePolicy(sizePolicy)
        self.verticalLayout = QtGui.QVBoxLayout(Param_Pulse)
        self.verticalLayout.setContentsMargins(-1, 24, -1, -1)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.threshold_spinbox = QtGui.QDoubleSpinBox(Param_Pulse)
        self.threshold_spinbox.setDecimals(2)
        self.threshold_spinbox.setMaximum(655.35)
        self.threshold_spinbox.setObjectName(_fromUtf8("threshold_spinbox"))
        self.gridLayout.addWidget(self.threshold_spinbox, 0, 1, 1, 1)
        self.label_9 = QtGui.QLabel(Param_Pulse)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout.addWidget(self.label_9, 0, 0, 1, 1)
        self.label_5 = QtGui.QLabel(Param_Pulse)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 1, 0, 1, 1)
        self.label_10 = QtGui.QLabel(Param_Pulse)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_10.setFont(font)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.gridLayout.addWidget(self.label_10, 2, 0, 1, 1)
        self.label_23 = QtGui.QLabel(Param_Pulse)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_23.setFont(font)
        self.label_23.setObjectName(_fromUtf8("label_23"))
        self.gridLayout.addWidget(self.label_23, 3, 0, 1, 1)
        self.debounce_spinbox = QtGui.QDoubleSpinBox(Param_Pulse)
        self.debounce_spinbox.setDecimals(0)
        self.debounce_spinbox.setMaximum(255.0)
        self.debounce_spinbox.setSingleStep(1.0)
        self.debounce_spinbox.setObjectName(_fromUtf8("debounce_spinbox"))
        self.gridLayout.addWidget(self.debounce_spinbox, 2, 1, 1, 1)
        self.hysteresis_spinbox = QtGui.QDoubleSpinBox(Param_Pulse)
        self.hysteresis_spinbox.setDecimals(2)
        self.hysteresis_spinbox.setMaximum(655.35)
        self.hysteresis_spinbox.setObjectName(_fromUtf8("hysteresis_spinbox"))
        self.gridLayout.addWidget(self.hysteresis_spinbox, 1, 1, 1, 1)
        self.edge_comboBox = QtGui.QComboBox(Param_Pulse)
        self.edge_comboBox.setObjectName(_fromUtf8("edge_comboBox"))
        self.edge_comboBox.addItem(_fromUtf8(""))
        self.edge_comboBox.addItem(_fromUtf8(""))
        self.edge_comboBox.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.edge_comboBox, 3, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)

        self.retranslateUi(Param_Pulse)
        QtCore.QMetaObject.connectSlotsByName(Param_Pulse)
        Param_Pulse.setTabOrder(self.threshold_spinbox, self.hysteresis_spinbox)
        Param_Pulse.setTabOrder(self.hysteresis_spinbox, self.debounce_spinbox)

    def retranslateUi(self, Param_Pulse):
        self.threshold_spinbox.setSuffix(_translate("Param_Pulse", " mV", None))
        self.label_9.setText(_translate("Param_Pulse", "Threshold", None))
        self.label_5.setText(_translate("Param_Pulse", "Hysteresis", None))
        self.label_10.setText(_translate("Param_Pulse", "Debounce time", None))
        self.label_23.setText(_translate("Param_Pulse", "Trigger edge", None))
        self.debounce_spinbox.setSuffix(_translate("Param_Pulse", " ms", None))
        self.hysteresis_spinbox.setSuffix(_translate("Param_Pulse", " mV", None))
        self.edge_comboBox.setItemText(0, _translate("Param_Pulse", "rising", None))
        self.edge_comboBox.setItemText(1, _translate("Param_Pulse", "falling", None))
        self.edge_comboBox.setItemText(2, _translate("Param_Pulse", "rising and falling", None))

