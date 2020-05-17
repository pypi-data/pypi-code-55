import logging


logger = logging.getLogger(__name__)


class Prueba:
    """ grupos de sub-pruebas incluidas en WISC """
    def __init__(self, name=None, code=None):
        self.name = name
        self.code = code
        # subpruebas ordenadas
        self.subpruebas = []

    def load_from_dict(self, data):
        self.name = data['name']
        self.code = data['code']
        subpruebas_ordenadas = sorted(data['subtests'], key=lambda k: k['orden']) 
        for subprueba in subpruebas_ordenadas:
            s = SubPrueba()
            s.load_from_dict(prueba=self, data=subprueba)
            self.subpruebas.append(s)


class SubPrueba:
    """ cada una de las sub-pruebas de WISC """
    def __init__(self, prueba=None, name=None, code=None, mandatory=None, orden=0):
        self.prueba = prueba
        self.name = name
        self.code = code
        self.mandatory = mandatory
        self.orden = orden

        # transformador de puntuación directa a puntuación escalar
        self.puntuacion_escalar = {}
    
    def load_from_dict(self, prueba, data):
        self.prueba = prueba
        self.name = data['name']
        self.code = data['code']
        self.orden = data['orden']
        self.mandatory = data['mandatory']
