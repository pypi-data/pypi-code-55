import json
import logging
import os

from datetime import datetime
from pywisc.tools.csv_drive import DriveCSV


logger = logging.getLogger(__name__)


class TablaEscalar:
    """ Tablas con datos para obtencion de los puntos escalares """

    def __init__(self, wisc, meses):
        """ Inicializacion
            Params:
                wisc = Version específica de WISC a usar
                meses = Cargar la tabla correspondiente a los meses del paciente
        """
        self.wisc = wisc
        self.meses = meses

        # datos de la tabla de datos para transoformar directa en escalar
        self.data = None
        self.load_data()
    
    def load_escalares(self):
        """ cargar la info de las tablas escalares disponibles """
        ver = self.wisc.version
        lang = self.wisc.language
        here = os.path.dirname(os.path.realpath(__file__))
        df = os.path.join(here, 'data', f'data_{ver}_{lang}.json')
        f = open(df, 'r')
        infos = json.loads(f.read())
        f.close()
        return infos
    
    def load_data(self):
        """ encontrar cual de todas las tablas de escalares corresponde con la edad del paciente """

        info = None
        infos_escalares = self.load_escalares()
        for esc in infos_escalares:
            if self.meses >= esc['from_months']:
                if self.meses <= esc['to_months']:
                    info = esc
        if info is None:
            raise ValueError(f'No se encontro la tabla de escalares para un paciente de {self.meses} meses')
        
        code = info['code']
        uid = info['drive_uid']
        gid = info['drive_gid']
        drive_name = f'wisc-{self.wisc.version}-{self.wisc.language}-{self.wisc.country}-{code}'
        d = DriveCSV(name=drive_name,
                 unique_id_column='Escalar',
                 uid=uid, gid=gid)
        self.data = d.tree
        return d.tree