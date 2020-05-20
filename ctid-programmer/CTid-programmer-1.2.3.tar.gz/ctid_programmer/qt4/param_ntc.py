# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CTid_Param_NTC.ui'
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

class Ui_Param_NTC(object):
    def setupUi(self, Param_NTC):
        Param_NTC.setObjectName(_fromUtf8("Param_NTC"))
        Param_NTC.resize(408, 369)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Param_NTC.sizePolicy().hasHeightForWidth())
        Param_NTC.setSizePolicy(sizePolicy)
        self.verticalLayout = QtGui.QVBoxLayout(Param_NTC)
        self.verticalLayout.setContentsMargins(-1, 24, -1, -1)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBox = QtGui.QGroupBox(Param_NTC)
        self.groupBox.setFlat(False)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout = QtGui.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_9 = QtGui.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout.addWidget(self.label_9, 0, 0, 1, 1)
        self.label_10 = QtGui.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_10.setFont(font)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.gridLayout.addWidget(self.label_10, 2, 0, 1, 1)
        self.label_5 = QtGui.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 1, 0, 1, 1)
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setOpenExternalLinks(True)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 1)
        self.ntc_b_lineEdit = QtGui.QLineEdit(self.groupBox)
        self.ntc_b_lineEdit.setObjectName(_fromUtf8("ntc_b_lineEdit"))
        self.gridLayout.addWidget(self.ntc_b_lineEdit, 1, 1, 1, 1)
        self.ntc_a_lineEdit = QtGui.QLineEdit(self.groupBox)
        self.ntc_a_lineEdit.setObjectName(_fromUtf8("ntc_a_lineEdit"))
        self.gridLayout.addWidget(self.ntc_a_lineEdit, 0, 1, 1, 1)
        self.ntc_c_lineEdit = QtGui.QLineEdit(self.groupBox)
        self.ntc_c_lineEdit.setObjectName(_fromUtf8("ntc_c_lineEdit"))
        self.gridLayout.addWidget(self.ntc_c_lineEdit, 2, 1, 1, 1)
        self.verticalLayout.addWidget(self.groupBox)
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.label_23 = QtGui.QLabel(Param_NTC)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_23.setFont(font)
        self.label_23.setTextFormat(QtCore.Qt.AutoText)
        self.label_23.setObjectName(_fromUtf8("label_23"))
        self.gridLayout_2.addWidget(self.label_23, 0, 0, 1, 1)
        self.label = QtGui.QLabel(Param_NTC)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_2.addWidget(self.label, 1, 0, 1, 1)
        self.label1 = QtGui.QLabel(Param_NTC)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label1.setFont(font)
        self.label1.setTextFormat(QtCore.Qt.AutoText)
        self.label1.setObjectName(_fromUtf8("label1"))
        self.gridLayout_2.addWidget(self.label1, 2, 0, 1, 1)
        self.ntc_m_lineEdit = QtGui.QLineEdit(Param_NTC)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ntc_m_lineEdit.sizePolicy().hasHeightForWidth())
        self.ntc_m_lineEdit.setSizePolicy(sizePolicy)
        self.ntc_m_lineEdit.setObjectName(_fromUtf8("ntc_m_lineEdit"))
        self.gridLayout_2.addWidget(self.ntc_m_lineEdit, 0, 1, 1, 1)
        self.ntc_n_lineEdit = QtGui.QLineEdit(Param_NTC)
        self.ntc_n_lineEdit.setObjectName(_fromUtf8("ntc_n_lineEdit"))
        self.gridLayout_2.addWidget(self.ntc_n_lineEdit, 1, 1, 1, 1)
        self.ntc_k_lineEdit = QtGui.QLineEdit(Param_NTC)
        self.ntc_k_lineEdit.setObjectName(_fromUtf8("ntc_k_lineEdit"))
        self.gridLayout_2.addWidget(self.ntc_k_lineEdit, 2, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_2)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(Param_NTC)
        QtCore.QMetaObject.connectSlotsByName(Param_NTC)
        Param_NTC.setTabOrder(self.ntc_a_lineEdit, self.ntc_b_lineEdit)
        Param_NTC.setTabOrder(self.ntc_b_lineEdit, self.ntc_c_lineEdit)
        Param_NTC.setTabOrder(self.ntc_c_lineEdit, self.ntc_m_lineEdit)
        Param_NTC.setTabOrder(self.ntc_m_lineEdit, self.ntc_n_lineEdit)
        Param_NTC.setTabOrder(self.ntc_n_lineEdit, self.ntc_k_lineEdit)

    def retranslateUi(self, Param_NTC):
        self.groupBox.setTitle(_translate("Param_NTC", "Steinhart-Hart Coefficients", None))
        self.label_9.setText(_translate("Param_NTC", "A", None))
        self.label_10.setText(_translate("Param_NTC", "C", None))
        self.label_5.setText(_translate("Param_NTC", "B", None))
        self.label_2.setText(_translate("Param_NTC", "<a href=\"https://www.thinksrs.com/downloads/programs/therm%20calc/ntccalibrator/ntccalculator.html\">Look up coefficients</a>", None))
        self.ntc_b_lineEdit.setPlaceholderText(_translate("Param_NTC", "[1/K]", None))
        self.ntc_a_lineEdit.setPlaceholderText(_translate("Param_NTC", "[1/K]", None))
        self.ntc_c_lineEdit.setPlaceholderText(_translate("Param_NTC", "[1/K]", None))
        self.label_23.setText(_translate("Param_NTC", "M", None))
        self.label.setText(_translate("Param_NTC", "N", None))
        self.label1.setText(_translate("Param_NTC", "K", None))
        self.ntc_m_lineEdit.setPlaceholderText(_translate("Param_NTC", "M parameter [V]", None))
        self.ntc_n_lineEdit.setPlaceholderText(_translate("Param_NTC", "N parameter [V/Ω]", None))
        self.ntc_k_lineEdit.setPlaceholderText(_translate("Param_NTC", "K parameter [1/Ω]", None))

