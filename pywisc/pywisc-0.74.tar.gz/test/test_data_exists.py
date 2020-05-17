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
