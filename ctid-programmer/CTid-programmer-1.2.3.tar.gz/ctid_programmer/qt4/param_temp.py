# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CTid_Param_Temp.ui'
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

class Ui_Param_Temp(object):
    def setupUi(self, Param_Temp):
        Param_Temp.setObjectName(_fromUtf8("Param_Temp"))
        Param_Temp.resize(318, 95)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Param_Temp.sizePolicy().hasHeightForWidth())
        Param_Temp.setSizePolicy(sizePolicy)
        self.horizontalLayout = QtGui.QHBoxLayout(Param_Temp)
        self.horizontalLayout.setContentsMargins(-1, 24, -1, -1)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.offset_spinbox = QtGui.QDoubleSpinBox(Param_Temp)
        self.offset_spinbox.setDecimals(6)
        self.offset_spinbox.setMinimum(-1000000000.0)
        self.offset_spinbox.setMaximum(1000000000.0)
        self.offset_spinbox.setObjectName(_fromUtf8("offset_spinbox"))
        self.gridLayout.addWidget(self.offset_spinbox, 1, 1, 1, 1)
        self.label_5 = QtGui.QLabel(Param_Temp)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 1, 0, 1, 1)
        self.label_9 = QtGui.QLabel(Param_Temp)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout.addWidget(self.label_9, 0, 0, 1, 1)
        self.scale_spinbox = QtGui.QDoubleSpinBox(Param_Temp)
        self.scale_spinbox.setDecimals(9)
        self.scale_spinbox.setMinimum(-1000000000.0)
        self.scale_spinbox.setMaximum(1000000000.0)
        self.scale_spinbox.setObjectName(_fromUtf8("scale_spinbox"))
        self.gridLayout.addWidget(self.scale_spinbox, 0, 1, 1, 1)
        self.gridLayout.setColumnStretch(0, 1)
        self.horizontalLayout.addLayout(self.gridLayout)

        self.retranslateUi(Param_Temp)
        QtCore.QMetaObject.connectSlotsByName(Param_Temp)
        Param_Temp.setTabOrder(self.scale_spinbox, self.offset_spinbox)

    def retranslateUi(self, Param_Temp):
        self.offset_spinbox.setSuffix(_translate("Param_Temp", " °C", None))
        self.label_5.setText(_translate("Param_Temp", "Offset", None))
        self.label_9.setText(_translate("Param_Temp", "Scale", None))
        self.scale_spinbox.setSuffix(_translate("Param_Temp", " °C/V", None))

