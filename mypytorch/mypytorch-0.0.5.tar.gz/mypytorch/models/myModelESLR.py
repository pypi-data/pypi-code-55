from .myModelES import MyModelES
from .myModelLR import MyModelLR


class MyModelESLR(MyModelES, MyModelLR):
    """ Model with early stopping and lr scheduler. """
