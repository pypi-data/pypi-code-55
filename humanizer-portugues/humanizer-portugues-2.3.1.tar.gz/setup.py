# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['humanizer_portugues']

package_data = \
{'': ['*']}

extras_require = \
{':python_version < "3.8"': ['importlib_metadata>=1.6.0,<2.0.0']}

setup_kwargs = {
    'name': 'humanizer-portugues',
    'version': '2.3.1',
    'description': 'Humanize functions for Portuguese.',
    'long_description': "# humanizer-portugues\n\n[![Tests](https://github.com/staticdev/humanizer-portugues/workflows/Tests/badge.svg)](https://github.com/staticdev/humanizer-portugues/actions?workflow=Tests)\n[![Codecov](https://codecov.io/gh/staticdev/humanizer-portugues/badge.svg?branch=master&service=github)](https://codecov.io/gh/staticdev/humanizer-portugues)\n![PyPi](https://badge.fury.io/py/humanizer-portugues.svg)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)\n\nEste pacote contém várias funções de humanização (humanization), como\ntransformar um número em uma duração legível para humanos ('três minutos\natrás') ou em uma frase. Ele funciona em python3, sendo recomendado\no uso da versão mais recente.\n\nEste código é baseado no pacote original\n[humanize](https://github.com/jmoiron/humanize), com atualização para\npython3, correções de tradução, formato e adição de humanização de\nlistas. Além disso, foi retirado o recurso de localização (i18n)\nfacilitando sua utilização para português.\n\n## Instalação\n\nPara instalar o `humanizer-portugues` execute o comando:\n\n```sh\npip install humanizer-portugues\n```\n\n## Uso\n\nPara importar o pacote basta executar:\n\n```python\nimport humanizer_portugues\n```\n\nHumanization de inteiros:\n\n```python\nhumanizer_portugues.int_comma(12345)\n'12,345'\n\nhumanizer_portugues.int_word(123455913)\n'123.5 milhão'\n\nhumanizer_portugues.int_word(12345591313)\n'12.3 bilhão'\n\nhumanizer_portugues.ap_number(4)\n'quatro'\n\nhumanizer_portugues.ap_number(41)\n'41'\n```\n\nHumanization datas e horas:\n\n```python\nimport datetime\nhumanizer_portugues.natural_period(datetime.time(5, 30, 0).hour)\n'manhã'\n\nhumanizer_portugues.natural_clock(datetime.time(0, 30, 0))\n'zero hora e trinta minutos'\n\nhumanizer_portugues.natural_clock(datetime.time(0, 30, 0), formal=False)\n'meia noite e meia'\n\nhumanizer_portugues.natural_day(datetime.datetime.now())\n'hoje'\n\nhumanizer_portugues.natural_delta(datetime.timedelta(seconds=1001))\n'16 minutos'\n\nhumanizer_portugues.natural_day(datetime.datetime.now() - datetime.timedelta(days=1))\n'ontem'\n\nhumanizer_portugues.natural_day(datetime.date(2007, 6, 5))\n'5 de junho'\n\nhumanizer_portugues.natural_date(datetime.date(2007, 6, 5))\n'5 de junho de 2007'\n\nhumanizer_portugues.natural_time(datetime.datetime.now() - datetime.timedelta(seconds=1))\n'há um segundo'\n\nhumanizer_portugues.natural_time(datetime.datetime.now() - datetime.timedelta(seconds=3600))\n'há uma hora'\n```\n\nHumanization de tamanho de arquivos:\n\n```python\nhumanizer_portugues.natural_size(1000000)\n'1.0 MB'\n\nhumanizer_portugues.natural_size(1000000, binary=True)\n'976.6 KiB'\n\nhumanizer_portugues.natural_size(1000000, gnu=True)\n'976.6K'\n```\n\nHumanization de números de ponto flutuante:\n\n```python\nhumanizer_portugues.fractional(1/3)\n'1/3'\n\nhumanizer_portugues.fractional(1.5)\n'1 1/2'\n\nhumanizer_portugues.fractional(0.3)\n'3/10'\n\nhumanizer_portugues.fractional(0.333)\n'333/1000'\n\nhumanizer_portugues.fractional(1)\n'1'\n```\n\nHumanization de listas:\n\n```python\nhumanizer_portugues.natural_list(['Cláudio', 'Maria'], ',')\n'Cláudio, Maria'\n\nhumanizer_portugues.natural_list(['Cláudio', 'Maria'], ',', 'e')\n'Cláudio e Maria'\n\nhumanizer_portugues.natural_list(['Cláudio', 'Maria', 'José'], ';', 'ou')\n'Cláudio; Maria ou José'\n```\n",
    'author': "Thiago Carvalho D'Ávila",
    'author_email': 'thiagocavila@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/staticdev/humanizer-portugues',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
