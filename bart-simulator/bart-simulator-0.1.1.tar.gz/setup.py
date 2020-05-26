# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['simulator', 'simulator.generate', 'simulator.send_data_ga', 'simulator.utils']

package_data = \
{'': ['*']}

install_requires = \
['faker>=4.1.0,<5.0.0', 'pandas>=1.0.3,<2.0.0', 'requests>=2.23.0,<3.0.0']

entry_points = \
{'console_scripts': ['simulator = simulator.main:main']}

setup_kwargs = {
    'name': 'bart-simulator',
    'version': '0.1.1',
    'description': 'Send event views to Google Analytics and Generator customers or products',
    'long_description': "# Bart Simulator (CLI)\n\n[![PyPI version](https://badge.fury.io/py/bart-simulator.svg)](https://badge.fury.io/py/bart-simulator)\n\nSend event views to Google Analytics and Generator customers or products\n\n## Install\n```\n$ pip install bart-simulator\n```\n\n## Usage\n\n```\nusage: simulator [-h] [--loglevel LOGLEVEL] [--version]  ...\n\nSend event views to Google Analytics and Generator customers or products data-\nset (bart-recs CLI)\n\noptional arguments:\n  -h, --help           show this help message and exit\n  --loglevel LOGLEVEL\n  --version            show program's version number and exit\n\nCommands:\n\n    generation         Gera os data set simulados para as recomendações\n    send-data-ga       Envia dados simulados para o Google Analytics\n```\n\n#### Generate DataSets\n```\n# Generation customers csv\n$ simulator generation customers -f csv\n\n# Generation customers json\n$ simulator generation customers -f json\n\n# Generation products csv\n$ simulator generation products -f csv\n\n# Generation products json\n$ simulator generation products -f json\n\n```\n#### Full Options\n```\nusage: simulator generation [-h] [--desc-path DESC_PATH] [--rows ROWS]\n                            --format {csv,json} [{csv,json} ...]\n                            {customers,products}\n\npositional arguments:\n  {customers,products}  Arquivo que sera gerado pelo processo\n\noptional arguments:\n  -h, --help            show this help message and exit\n  --desc-path DESC_PATH, -d DESC_PATH\n                        Pasta onde sera salvo os dataset gerados\n  --rows ROWS, -r ROWS  Quantidades de Linhas geradas\n  --format {csv,json} [{csv,json} ...], -f {csv,json} [{csv,json} ...]\n                        Formato do arquivo de saida que sera salvo,pode ser\n                        adiciona mais de um tipo ao mesmo tempo\n```\n\n#### Send events to GA\n\n```\n$ simulator send-data-ga pageview \\\n    -c https://github.com/cesarbruschetta/bart-recs/datasets/customers.csv \\\n    -p https://github.com/cesarbruschetta/bart-recs/datasets/products.csv \\\n    -i 10\n```\n\n#### Full Options\n```\nusage: simulator send-data-ga [-h] --customers CUSTOMERS --products PRODUCTS\n                              [--interactions INTERACTIONS]\n                              {pageview}\n\npositional arguments:\n  {pageview}            Tipo de evento que sera enviado ao GA\n\noptional arguments:\n  -h, --help            show this help message and exit\n  --customers CUSTOMERS, -c CUSTOMERS\n                        Caminho para o dataset de customers, em csv\n  --products PRODUCTS, -p PRODUCTS\n                        Caminho para o dataset de products, em csv\n  --interactions INTERACTIONS, -i INTERACTIONS\n                        Quantidades de interações geradas\n```\n\n\n\n## Licence\n[Apache License](./LICENSE) - Version 2.0, January 2004 \n\n",
    'author': 'Cesar Augusto',
    'author_email': 'cesarabruschetta@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/cesarbruschetta/bart-recs',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
