import os

from pywisc.evaluacion import Evaluacion
from pywisc.wisc import Wisc


def main():
    print("##########################")
    print("Calculador WISC 4. Versión español, Argentina")
    print("##########################")
    w = Wisc(wisc_version=4, language='es', country='ar')
    e = Evaluacion(wisc=w)
    e.ask_directas_as_terminal()