import pandas as pd

forms = {
    'water': {'liq': 0,
              'gas': 1,
              'saturado': 2
              },

    'air': {'gas': 0
            },

    'r134a': {'gas': 0,
              'saturado': 1,
              },

    'nh3': {'gas': 0,
            'saturado': 1,
            },
    'co2': {'gas': 0,
            'saturado': 1,
            }
}


formspd = pd.DataFrame.from_dict(forms)
formspd = formspd.fillna('-')
print('O Atha é lindo, me siguam no insta @victorathanasio')
print()
print('Baixe e coloque o chromedriver.exe no seu path (ou na mesma pasta que seu .py), importantíssmo, se não, não funciona')
print()
print('As combinações de estado e de material estão indicadas por números na tabela abaixo,')
print(formspd)
print()
print('para usar os estados, use: from state_calculator import *')
print()
print('para iniciar use variavel = estado(material, table, p=pressão(Kpa), T=temperatura(celsius)')
print()
print('Nao se esqueça de fechar, MUITO IMPORTANTE: variavel.quit()')
print('só precisa fechar uma das variáveis, o sistema como um todo fecha, e não é possível fazer mais requisições')
from .estado import *