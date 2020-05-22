import qtpy
import qtpy.QtWidgets
import qtpy.QtCore


class Test(qtpy.QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        qtpy.QtCore.QTimer.singleShot(100, self.test)

        def test2():
            print('inner function')

        qtpy.QtCore.QTimer.singleShot(100, test2)

    def test(self):
        print('test called / bound method')


app = qtpy.QtWidgets.QApplication([])

test = Test()
test.deleteLater()
del test
test = None

app.exec_()

