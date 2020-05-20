# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ctid_programmer/qt4/egauge_api_credentials_dialog.ui'
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

class Ui_Credentials_Dialog(object):
    def setupUi(self, Credentials_Dialog):
        Credentials_Dialog.setObjectName(_fromUtf8("Credentials_Dialog"))
        Credentials_Dialog.resize(307, 174)
        self.gridLayout = QtGui.QGridLayout(Credentials_Dialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.buttonBox = QtGui.QDialogButtonBox(Credentials_Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 3, 0, 1, 2)
        self.label = QtGui.QLabel(Credentials_Dialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)
        self.label_3 = QtGui.QLabel(Credentials_Dialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.username_lineEdit = QtGui.QLineEdit(Credentials_Dialog)
        self.username_lineEdit.setObjectName(_fromUtf8("username_lineEdit"))
        self.gridLayout.addWidget(self.username_lineEdit, 1, 1, 1, 1)
        self.password_lineEdit = QtGui.QLineEdit(Credentials_Dialog)
        self.password_lineEdit.setInputMask(_fromUtf8(""))
        self.password_lineEdit.setText(_fromUtf8(""))
        self.password_lineEdit.setEchoMode(QtGui.QLineEdit.Password)
        self.password_lineEdit.setObjectName(_fromUtf8("password_lineEdit"))
        self.gridLayout.addWidget(self.password_lineEdit, 2, 1, 1, 1)
        self.prompt_label = QtGui.QLabel(Credentials_Dialog)
        self.prompt_label.setWordWrap(True)
        self.prompt_label.setObjectName(_fromUtf8("prompt_label"))
        self.gridLayout.addWidget(self.prompt_label, 0, 0, 1, 2)

        self.retranslateUi(Credentials_Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Credentials_Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Credentials_Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Credentials_Dialog)

    def retranslateUi(self, Credentials_Dialog):
        Credentials_Dialog.setWindowTitle(_translate("Credentials_Dialog", "eGauge API Login", None))
        self.label.setText(_translate("Credentials_Dialog", "Password", None))
        self.label_3.setText(_translate("Credentials_Dialog", "Username", None))
        self.prompt_label.setText(_translate("Credentials_Dialog", "Please enter your eGuard username and password.", None))

