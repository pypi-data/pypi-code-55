# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_zarinpal', 'django_zarinpal.migrations']

package_data = \
{'': ['*']}

install_requires = \
['django-hashid-field>=3.1.1,<4.0.0', 'zeep>=3.4.0,<4.0.0']

setup_kwargs = {
    'name': 'django-zarinpal',
    'version': '1.0.1',
    'description': 'integrate django payments with zarrinpal',
    'long_description': '# django-zarinpal\n\nIntegrate django payments with [zarinpal](https://www.zarinpal.com)\n\n\nFeatures\n--------\n\n- sending signal on verifying transaction to let other apps know about it\n\nQuickstart\n----------\n\nInstall django-zarinpal::\n\n    pip install django-zarinpal\n\nAdd it to your `INSTALLED_APPS`:\n\n.. code-block:: python\n\n    INSTALLED_APPS = (\n        ...\n        \'zarinpal\',\n        ...\n    )\n\nAdd django-zarinpal\'s URL patterns:\n\n.. code-block:: python\n\n    import zarrinpal\n\n\n    urlpatterns = [\n        ...\n        path(\'zarinpal/\', include(zarinpal_urls)),\n        ...\n    ]\n\n\n\n### How to Use\n\nset these variables in your settings file:\n\n```python\n\nZARINPAL_CALLBACK_URL: bool # the url user redirects to after transaction\n\nZARINPAL_SIMULATION: bool # is transactions for test?\n\nZARINPAL_MERCHANT_ID: str # merchant id from zarinpal (you may leave it blank if you set the simulation to True)\n```\n\nyou can use function `start_transaction` with a dictionary containing your transaction data like this:\n\n```python\nfrom django.shortcuts import redirect\nfrom django_zarinpal.services import start_transaction\n\n\ndef start_payment(request):\n    result = start_transaction(\n        {\n            "user": request.user,\n            "amount": 10000,\n            "description": "transaction description",\n            "mobile": "09123456789",\n            "email": "string",\n        }\n    )\n    return redirect(result) # result is the url for starting transaction\n```\n\nIf you specify a callback_url in transaction data after completing transaction zarinpal will redirect user to the page you specified with two get arguments:\n\n1.order_number: str\n\n2.success: boolean\n\n### Custom verification\n\nIf you want to handle verifying transaction your self you can define your view and \naddress it in settings with ZARINPAL_VERIFY_TRANSACTION_VIEW. you can use function\n`verify_transaction` to verify a transaction.\n\nIf you don\'t specify this view, package will use default view for verifying transactions.\n\nTests\n--------\nRunning tests: ::\n\n    python manage.py runtests.py\n',
    'author': 'glyphack',
    'author_email': 'sh.hooshyari@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
