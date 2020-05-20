# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ctid_programmer/qt4/preferences_dialog.ui'
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

class Ui_Preferences_Dialog(object):
    def setupUi(self, Preferences_Dialog):
        Preferences_Dialog.setObjectName(_fromUtf8("Preferences_Dialog"))
        Preferences_Dialog.resize(281, 182)
        self.gridLayout = QtGui.QGridLayout(Preferences_Dialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(Preferences_Dialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.increment_spinbox = QtGui.QSpinBox(Preferences_Dialog)
        self.increment_spinbox.setMinimum(1)
        self.increment_spinbox.setMaximum(10000)
        self.increment_spinbox.setObjectName(_fromUtf8("increment_spinbox"))
        self.gridLayout.addWidget(self.increment_spinbox, 1, 1, 1, 1)
        self.station_id_spinbox = QtGui.QSpinBox(Preferences_Dialog)
        self.station_id_spinbox.setPrefix(_fromUtf8(""))
        self.station_id_spinbox.setMinimum(0)
        self.station_id_spinbox.setObjectName(_fromUtf8("station_id_spinbox"))
        self.gridLayout.addWidget(self.station_id_spinbox, 2, 1, 1, 1)
        self.label_2 = QtGui.QLabel(Preferences_Dialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(Preferences_Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 3, 0, 1, 2)
        self.sn_service_combo = QtGui.QComboBox(Preferences_Dialog)
        self.sn_service_combo.setObjectName(_fromUtf8("sn_service_combo"))
        self.sn_service_combo.addItem(_fromUtf8(""))
        self.sn_service_combo.addItem(_fromUtf8(""))
        self.sn_service_combo.setItemText(1, _fromUtf8("eGauge"))
        self.gridLayout.addWidget(self.sn_service_combo, 0, 1, 1, 1)
        self.label_3 = QtGui.QLabel(Preferences_Dialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)

        self.retranslateUi(Preferences_Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Preferences_Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Preferences_Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Preferences_Dialog)

    def retranslateUi(self, Preferences_Dialog):
        Preferences_Dialog.setWindowTitle(_translate("Preferences_Dialog", "Dialog", None))
        self.label.setText(_translate("Preferences_Dialog", "Serial-number increment", None))
        self.station_id_spinbox.setToolTip(_translate("Preferences_Dialog", "The serial-number modulo the serial-number increment must equal the station number.", None))
        self.label_2.setText(_translate("Preferences_Dialog", "Station id", None))
        self.sn_service_combo.setItemText(0, _translate("Preferences_Dialog", "none", None))
        self.label_3.setText(_translate("Preferences_Dialog", "Serial-number service to use", None))

