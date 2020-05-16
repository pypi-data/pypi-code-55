# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['squarespace_commerce']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.23.0,<3.0.0']

entry_points = \
{'console_scripts': ['build-backend = poetry.masonry.api',
                     'my-script = squarespace_commerce.app:start',
                     "requires = ['poetry>=0.12']"]}

setup_kwargs = {
    'name': 'squarespace-commerce',
    'version': '0.1.1',
    'description': 'Pythonic access to the Squarespace Commerce API',
    'long_description': "# Squarespace_Commerce Python Module\n\nThe Squarespace_Commerce module attempts to provide easy access to [Squarespace's Commerce API](http://developers.squarespace.com/commerce-api\n).\n\n## Usage\n````\n#Instantiate the squarespace class to get access to your store:\n#Version defaults to 1.5\norder = Squarespace('APIKEY')\n\n#Optional Parameters include:\norder = Squarespace('APIKEY','APIVERSION','APIBASEURL')\n````\n## Orders API\n````\n#Get the first page of orders, returns 50:\norder.get_orders()\n\n#Optional Parameters include:\norder.get_orders(cursor='{Token}',modified_after='{ISO 8601 Date}'',modified_before='{ISO 8601 Date}',fulfillment_status='{PENDING | FULFILLED | CANCELLED}')\n\n#Get a specific order\norder.get_order('order_id')\n\n#Fulfill a specific order\norder.fulfill_order('order_id')\n\n#Optional Parameters include:\norder.fulfill_order('order_id', send_notification={True | FALSE}, ship_date={ISO 8601 Date}, tracking_number='',\n                      carrier_name='', service='', tracking_url='{valid_url}'):\n````\n## Transactions API\n#WIP\n\n\n## Inventory API\n#WIP\n",
    'author': 'Casey Dierking',
    'author_email': 'casey@dierking.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://https://github.com/caseydierking/squarespace-commerce-python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
