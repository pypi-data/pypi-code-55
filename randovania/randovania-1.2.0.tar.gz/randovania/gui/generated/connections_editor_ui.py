# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/travis/build/randovania/randovania/randovania/gui/ui_files/connections_editor.ui',
# licensing of '/home/travis/build/randovania/randovania/randovania/gui/ui_files/connections_editor.ui' applies.
#
# Created: Sun May 24 21:36:57 2020
#      by: pyside2-uic  running on PySide2 5.12.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_ConnectionEditor(object):
    def setupUi(self, ConnectionEditor):
        ConnectionEditor.setObjectName("ConnectionEditor")
        ConnectionEditor.resize(600, 300)
        ConnectionEditor.setMinimumSize(QtCore.QSize(600, 0))
        self.gridLayout_2 = QtWidgets.QGridLayout(ConnectionEditor)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.visualizer_scroll = QtWidgets.QScrollArea(ConnectionEditor)
        self.visualizer_scroll.setWidgetResizable(True)
        self.visualizer_scroll.setObjectName("visualizer_scroll")
        self.visualizer_contents = QtWidgets.QWidget()
        self.visualizer_contents.setGeometry(QtCore.QRect(0, 0, 494, 280))
        self.visualizer_contents.setObjectName("visualizer_contents")
        self.contents_layout = QtWidgets.QVBoxLayout(self.visualizer_contents)
        self.contents_layout.setObjectName("contents_layout")
        self.visualizer_scroll.setWidget(self.visualizer_contents)
        self.gridLayout_2.addWidget(self.visualizer_scroll, 0, 0, 1, 1)
        self.button_box = QtWidgets.QDialogButtonBox(ConnectionEditor)
        self.button_box.setOrientation(QtCore.Qt.Vertical)
        self.button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.button_box.setObjectName("button_box")
        self.gridLayout_2.addWidget(self.button_box, 0, 1, 1, 1)

        self.retranslateUi(ConnectionEditor)
        QtCore.QObject.connect(self.button_box, QtCore.SIGNAL("accepted()"), ConnectionEditor.accept)
        QtCore.QObject.connect(self.button_box, QtCore.SIGNAL("rejected()"), ConnectionEditor.reject)
        QtCore.QMetaObject.connectSlotsByName(ConnectionEditor)

    def retranslateUi(self, ConnectionEditor):
        ConnectionEditor.setWindowTitle(QtWidgets.QApplication.translate("ConnectionEditor", "Connection Editor", None, -1))

