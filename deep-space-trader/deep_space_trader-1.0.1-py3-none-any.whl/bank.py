from deep_space_trader.items import ItemBrowser

from PyQt5 import QtWidgets, QtCore, QtGui


class Warehouse(QtWidgets.QWidget):
    def __init__(self, parent):
        super(Bank, self).__init__(parent)

        self.parent = parent
        self.mainLayout = QtWidgets.QVBoxLayout(self)
        self.mainLayout.
