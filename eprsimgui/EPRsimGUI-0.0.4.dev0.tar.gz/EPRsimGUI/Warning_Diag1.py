# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Warning_Diag1.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Warning_Diag1(object):
    def setupUi(self, Warning_Diag1):
        Warning_Diag1.setObjectName("Warning_Diag1")
        Warning_Diag1.resize(447, 120)
        Warning_Diag1.setStyleSheet("background-color: rgb(184, 184, 184);")
        self.pushButton = QtWidgets.QPushButton(Warning_Diag1)
        self.pushButton.setGeometry(QtCore.QRect(330, 90, 99, 27))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(Warning_Diag1)
        self.label.setGeometry(QtCore.QRect(110, 0, 241, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Warning_Diag1)
        self.label_2.setGeometry(QtCore.QRect(60, 40, 321, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")

        self.retranslateUi(Warning_Diag1)
        QtCore.QMetaObject.connectSlotsByName(Warning_Diag1)

    def retranslateUi(self, Warning_Diag1):
        _translate = QtCore.QCoreApplication.translate
        Warning_Diag1.setWindowTitle(_translate("Warning_Diag1", "Dimension Warning"))
        self.pushButton.setText(_translate("Warning_Diag1", "OK"))
        self.label.setText(_translate("Warning_Diag1", "Hilbert Space dimension is > 512"))
        self.label_2.setText(_translate("Warning_Diag1", "Simulation in the solid-state regime is not posssible!"))
