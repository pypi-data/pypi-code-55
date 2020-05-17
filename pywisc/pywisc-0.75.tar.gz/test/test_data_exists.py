from datetime import datetime, timedelta

from pywisc.wisc import Wisc
from pywisc.evaluacion import Evaluacion


def test_all_days():
    """ probar todos los dias desde los 6 a los 6 años y ver que exista una evaluacion
        incrementar gradualmente los puntos para probar a grandes rasgos que siempre el CI
            crece cuando crecen las puntuaciones directas
    """

    w = Wisc(wisc_version=4, language='es', country='ar')

    today = datetime.today()
    # TODO cargar las planillas de 16 años e incrementar esto
    end = 15 * 365 - 1
    start = 6 * 365

    # simulamos que los tests se hacen hoy
    test_date = today.strftime('%Y-%m-%d')

    for days_back in range(start, end):
        day = today - timedelta(days=days_back)
        
        born_date = day.strftime('%Y-%m-%d')
        e = Evaluacion(wisc=w)
        reqs = {'born_date': born_date, 'test_date': test_date}
        e.validate_reqs(reqs=reqs)
        e.calculate_age()
        
        if days_back % 100 == 0:  # CI platform limit max logs length
            print('{} Y{} m{} M{}'.format(born_date, e.data['years'], e.data['months'], e.data['full_months']))
        last_ci = 0
        for v in range(5, 26):  # 26 parece ser el menor de los máximos puntajes
            
            directas =  {'S': v, 'V': v, 'C': v, 'CC': v, 'Co': v, 'M': v, 'RD': v, 'LN': v, 'Cl': v, 'BS': v}

            new_ci = e.calculate_ci(directas=directas)
            if days_back % 100 == 0:  # CI platform limit max logs length
                print('{} {}>={}'.format(born_date, new_ci, last_ci))
            assert new_ci >= last_ci
            last_ci = new_ci


def test_all_columns():
    """ probar que todas las planillas tienen columnas 
        con valores que crecen siempre
    """

    w = Wisc(wisc_version=4, language='es', country='ar')

    today = datetime.today()
    # TODO cargar las planillas de 16 años e incrementar esto
    end = 15 * 365 - 1
    start = 6 * 365

    # simulamos que los tests se hacen hoy
    test_date = today.strftime('%Y-%m-%d')

    for days_back in range(start, end, 90):
        day = today - timedelta(days=days_back)
        
        born_date = day.strftime('%Y-%m-%d')
        e = Evaluacion(wisc=w)
        reqs = {'born_date': born_date, 'test_date': test_date}
        e.validate_reqs(reqs=reqs)
        # luego de calcular la edad se conecta con la tabla de equivalencias con los escalares
        e.calculate_age()
        
        data = e.tabla_escalar.data
        info = e.tabla_escalar.table_info

        keys =  ['S', 'V', 'C', 'CC', 'Co', 'M', 'RD', 'LN', 'Cl', 'BS']
        
        for k in keys:
            last_val = 0
            c = 0
            for row in data:
                c += 1
                print(f'Info: {info}. Row: {k}-{c} {row}')
                if row[k] != '':
                    new_val = int(row[k])
                    assert new_val >= last_val
                    last_val = new_val
