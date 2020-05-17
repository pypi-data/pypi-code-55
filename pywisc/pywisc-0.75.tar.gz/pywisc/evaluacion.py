import json
import logging
from datetime import datetime
from pywisc.tools.csv_drive import DriveCSV
from pywisc.escalares import TablaEscalar


logger = logging.getLogger(__name__)


class Evaluacion:
    """ Evaluacion de cada uno de los niñes evaluados """

    def __init__(self, wisc):
        """ Inicializacion
            Params:
                wisc = Version específica de WISC a usar
        """
        self.wisc = wisc

        # todos los datos cargados de este proceso
        self.data = {}
        # tabla final usada segun el test y la edad
        self.tabla_escalar = None

    def calculate_age(self):
        born_date = self.data['born_date']
        test_date = self.data['test_date']

        full_months = (test_date.year - born_date.year) * 12 + test_date.month - born_date.month
        years = full_months // 12
        months = full_months % 12
        logger.info(f'Total meses: {full_months}')
        logger.info(f'o {years} años y and {months}')
        self.data['full_months'] = full_months
        self.data['years'] = years
        self.data['months'] = months        

        # cargar la tabla de escalares para esta edad
        self.tabla_escalar = TablaEscalar(wisc=self.wisc, meses=self.data['full_months'])
    
    def calculate_escalar(self, code, directa):
        """ calcular un escalar para un código especifico con una puntuacion directa dada """
        escalar = None
        for row in self.tabla_escalar.data:
            if row[code] != '':
                val = int(row[code])
                logger.info(f'{val} vs {directa}')
                if val >= directa:
                    escalar = int(row['Escalar'])
                    break
        if escalar is None:
            raise ValueError(f'No se encontró el escalar para la directa={directa} para {code}')
    
        return escalar

    def calculate_ci(self, directas):
        """ Calcular total de CI en base a las escalares
            Param:
                directas: dict {'<str>code1', '<int>directa1', '<str>code2', '<int>directa2', ... }]
        """
        print(f'Calc over {directas}')
        ci = 0
        for code, directa in directas.items():
            ci += self.calculate_escalar(code=code, directa=directa)

        return ci

    def ask_requirements_as_terminal(self):
        """ cargar los datos requeridos y calcular los meses """
        rts = self.wisc.required_to_start
        
        # retorno a validar
        ret = {}
        
        for req in rts:
            text = req['text']
            fts = req['formats_txt_to_user']
            ask = f'{text} \n\tFormato: {fts}\n'
            if req['default'] is not None:
                if req['default'] == 'today':
                    dft = datetime.today().strftime("%Y-%m-%d")
                ask += f'\tPredeterminado: {dft}\n'
            
            s = input(ask)
            if s == '':
                if req['default'] is not None:
                    s = dft
                else:
                    raise ValueError('Debes completar el dato')
            
            if req['data_type'] == 'date':
                val = None
                for fmt in req['formats']:
                    try:
                        val = datetime.strptime(s, fmt)
                    except ValueError:
                        pass
                    if val is not None:
                        break

                if val is None:
                    raise ValueError('No coincide con ninguno de los formatos esperados')
        
                ret[req['code']] = s

        return ret

    def validate_reqs(self, reqs):
        """ ya tome los valores requeridos, ahora los cargo a self.data validados """
        rts = self.wisc.required_to_start
        for req in rts:
            if req['data_type'] == 'date':
                val = None
                for fmt in req['formats']:
                    try:
                        val = datetime.strptime(reqs[req['code']], fmt)
                    except ValueError:
                        pass
                    if val is not None:
                        break

                if val is None:
                    raise ValueError('No coincide con ninguno de los formatos esperados')
        
                self.data[req['code']] = val


    def ask_directas_as_terminal(self):
        """ ask required data to start """
        
        reqs = self.ask_requirements_as_terminal()
        self.validate_reqs(reqs=reqs)
        self.calculate_age()

        # tomar las puntuaciones directas y trasformarlas en escalares
        directas = {}
        for prueba in self.wisc.pruebas:
            # solo espero un numero entero por cada subtest
            for subprueba in prueba.subpruebas:
                name = '{}-{}'.format(prueba.name, subprueba.name)
                code = '{}-{}'.format(prueba.code, subprueba.code)
                
                if not subprueba.mandatory:
                    logger.info(f'Ignorando la prueba no obligatoria {name}')
                    continue

                ask = f'{name} ({code}):'
                directa = int(input(ask))                
                directas[subprueba.code] = directa

        # sumar escalares
        ci = self.calculate_ci(directas=directas)
        
        print(f'CI calculado: {ci}')
        
        # TODO test: con 10 en todas las directas el CI es 89