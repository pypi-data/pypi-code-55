# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ctid_programmer/qt4/template_dialog.ui'
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

class Ui_Template_Dialog(object):
    def setupUi(self, Template_Dialog):
        Template_Dialog.setObjectName(_fromUtf8("Template_Dialog"))
        Template_Dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        Template_Dialog.resize(809, 530)
        Template_Dialog.setModal(True)
        self.horizontalLayout_2 = QtGui.QHBoxLayout(Template_Dialog)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.template_name_frame = QtGui.QFrame(Template_Dialog)
        self.template_name_frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.template_name_frame.setFrameShadow(QtGui.QFrame.Raised)
        self.template_name_frame.setObjectName(_fromUtf8("template_name_frame"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.template_name_frame)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_2 = QtGui.QLabel(self.template_name_frame)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout.addWidget(self.label_2)
        self.lineEdit = QtGui.QLineEdit(self.template_name_frame)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.horizontalLayout.addWidget(self.lineEdit)
        self.verticalLayout_2.addWidget(self.template_name_frame)
        self.existing_templates_frame = QtGui.QFrame(Template_Dialog)
        self.existing_templates_frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.existing_templates_frame.setFrameShadow(QtGui.QFrame.Raised)
        self.existing_templates_frame.setObjectName(_fromUtf8("existing_templates_frame"))
        self.verticalLayout = QtGui.QVBoxLayout(self.existing_templates_frame)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(self.existing_templates_frame)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.listWidget = QtGui.QListWidget(self.existing_templates_frame)
        self.listWidget.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.listWidget.setObjectName(_fromUtf8("listWidget"))
        self.verticalLayout.addWidget(self.listWidget)
        self.verticalLayout_2.addWidget(self.existing_templates_frame)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.buttonBox = QtGui.QDialogButtonBox(Template_Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Open|QtGui.QDialogButtonBox.Save)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.horizontalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(Template_Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Template_Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Template_Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Template_Dialog)

    def retranslateUi(self, Template_Dialog):
        Template_Dialog.setWindowTitle(_translate("Template_Dialog", "CTid Templates", None))
        self.label_2.setText(_translate("Template_Dialog", "New template name:", None))
        self.label.setText(_translate("Template_Dialog", "Existing Templates (right click to rename or delete):", None))

