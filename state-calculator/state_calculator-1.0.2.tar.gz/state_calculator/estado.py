# %%

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
global browser
options = Options()
options.headless = True
options.add_argument('log-level=3')
browser = webdriver.Chrome('chromedriver.exe', options=options)

# %%

sites = {
    'water': 'https://www.peacesoftware.de/einigewerte/wasser_dampf_e.html',
    'air': 'https://www.peacesoftware.de/einigewerte/luft_e.html',
    'r134a': 'http://www.peacesoftware.de/einigewerte/r134a_e.html',
    'nh3': 'https://www.peacesoftware.de/einigewerte/nh3_e.html',
    'co2': 'https://www.peacesoftware.de/einigewerte/co2_e.html'
}

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
print('Baixe e coloque o chromedriver.exe no seu path, importantíssmo, se não não funciona')
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
# %%


# %%

class estado():
    def __init__(self, material, table, p=None, T=None):
        global browser
        self.browser = browser
        self.browser.get(sites[material])
        self._material = material
        self._table_name = table
        self._forms_id = forms[material][table]
        self._p = str(p/100)
        self._T = str(T)
        self.wrong = False
        # try:
        #     data_frame = self._get_properties()
        # except:
        #     self.wrong = True
        #     print('Verifique se as condições dão na tabela selecionada')
        self._get_properties()
        print(self)

    def _get_properties(self):
        p = self._p
        T = self._T
        input_forms = self.browser.find_elements_by_tag_name('form')[self._forms_id]
        input_table = input_forms.find_element_by_tag_name('table')
        inputs = input_table.find_elements_by_tag_name('input')
        confirm_btn = input_forms.find_elements_by_tag_name('input')[-1]
        if p != None:
            inputs[0].send_keys(p)
        if T != None:
            inputs[1].send_keys(T)
        confirm_btn.click()
        data_frame = pd.read_html(self.browser.page_source, header=0)[1]
        data_frame = data_frame.fillna('None')
        data_frame['Properties'] = data_frame.apply(lambda x: set_properties(x.Property, x.Value, x.Unit), axis=1)

        property_list = data_frame['Properties'].tolist()

        for property in property_list:
            a = property
            code = "self.{} = a[0]".format(a[0].name)
            code = code.replace("'", "")
            #print(code)
            exec(code)
        self.data_frame = data_frame
        self.data_frame = self.data_frame.drop('Properties', axis=1)

    def __str__(self):
        if not self.wrong:
            pressure = self.pressure
            temperature = self.temperature
            return 'Estado = {}, tabela: {}, Pressão = {} {}, Temperatura = {} {}'.format(self.medium.value,
                                                                                      self._table_name, pressure.value,
                                                                                      pressure.unit, temperature.value,
                                                                                      temperature.unit)
        else:
            return 'Tabela errada'

    def quit(self):
        self.browser.quit()

class Property():
    def __init__(self, name, value, unit):
        self.name = name
        self.value = value
        self.unit = unit

    def __str__(self):
        if self.unit != 'None':
            return '{} = {} {}'.format(self.name, self.value, self.unit)
        else:
            return '{} = {}'.format(self.name, self.value)


def set_properties(property, Value, Unit):
    if str(Unit) == 'nan':
        Unit = 'None'
    name = property.replace(':', '')
    name = name.replace(" ", '_')
    name = name.replace("-", '_').lower()
    name = name.replace("_(calculated)", '')
    name = name.replace("boiling_", '')

    if name[-1] == '_':
        name = name[:-1]
    try:
        value = float(Value)
    except:
        value = Value
    unit = Unit.replace('[', '')
    unit = unit.replace(']', '')

    return [Property(name, value, unit)]
