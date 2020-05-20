# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ctid_programmer/qt4/param_volt.ui'
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

class Ui_Param_Volt(object):
    def setupUi(self, Param_Volt):
        Param_Volt.setObjectName(_fromUtf8("Param_Volt"))
        Param_Volt.resize(318, 95)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Param_Volt.sizePolicy().hasHeightForWidth())
        Param_Volt.setSizePolicy(sizePolicy)
        self.horizontalLayout = QtGui.QHBoxLayout(Param_Volt)
        self.horizontalLayout.setContentsMargins(-1, 24, -1, -1)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_5 = QtGui.QLabel(Param_Volt)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 1, 0, 1, 1)
        self.scale_spinbox = QtGui.QDoubleSpinBox(Param_Volt)
        self.scale_spinbox.setDecimals(3)
        self.scale_spinbox.setMinimum(-1000000.0)
        self.scale_spinbox.setMaximum(1000000.0)
        self.scale_spinbox.setObjectName(_fromUtf8("scale_spinbox"))
        self.gridLayout.addWidget(self.scale_spinbox, 0, 1, 1, 1)
        self.label_9 = QtGui.QLabel(Param_Volt)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout.addWidget(self.label_9, 0, 0, 1, 1)
        self.offset_spinbox = QtGui.QDoubleSpinBox(Param_Volt)
        self.offset_spinbox.setDecimals(3)
        self.offset_spinbox.setMinimum(-1000000.0)
        self.offset_spinbox.setMaximum(1000000.0)
        self.offset_spinbox.setObjectName(_fromUtf8("offset_spinbox"))
        self.gridLayout.addWidget(self.offset_spinbox, 1, 1, 1, 1)
        self.label_10 = QtGui.QLabel(Param_Volt)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_10.setFont(font)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.gridLayout.addWidget(self.label_10, 2, 0, 1, 1)
        self.delay_spinbox = QtGui.QDoubleSpinBox(Param_Volt)
        self.delay_spinbox.setDecimals(2)
        self.delay_spinbox.setMinimum(-327.68)
        self.delay_spinbox.setMaximum(327.67)
        self.delay_spinbox.setObjectName(_fromUtf8("delay_spinbox"))
        self.gridLayout.addWidget(self.delay_spinbox, 2, 1, 1, 1)
        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 1)
        self.horizontalLayout.addLayout(self.gridLayout)

        self.retranslateUi(Param_Volt)
        QtCore.QMetaObject.connectSlotsByName(Param_Volt)
        Param_Volt.setTabOrder(self.scale_spinbox, self.offset_spinbox)
        Param_Volt.setTabOrder(self.offset_spinbox, self.delay_spinbox)

    def retranslateUi(self, Param_Volt):
        self.label_5.setText(_translate("Param_Volt", "Offset", None))
        self.scale_spinbox.setSuffix(_translate("Param_Volt", " V/V", None))
        self.label_9.setText(_translate("Param_Volt", "Scale", None))
        self.offset_spinbox.setSuffix(_translate("Param_Volt", " V", None))
        self.label_10.setText(_translate("Param_Volt", "Delay", None))
        self.delay_spinbox.setSuffix(_translate("Param_Volt", " μs", None))

