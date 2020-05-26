# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['getpaid',
 'getpaid.backends',
 'getpaid.backends.dummy',
 'getpaid.migrations',
 'getpaid.templatetags']

package_data = \
{'': ['*'], 'getpaid.backends.dummy': ['templates/getpaid_dummy/*']}

install_requires = \
['django-fsm>=2.7.0,<3.0.0',
 'django-model-utils>=4.0.0,<5.0.0',
 'pendulum>=2.0.5,<3.0.0',
 'swapper>=1.1.2,<2.0.0',
 'typing-extensions>=3.7.4,<4.0.0']

setup_kwargs = {
    'name': 'django-getpaid',
    'version': '2.2.1',
    'description': 'Multi-broker payment processor for Django.',
    'long_description': '.. image:: https://img.shields.io/pypi/v/django-getpaid.svg\n    :target: https://pypi.org/project/django-getpaid/\n    :alt: Latest PyPI version\n.. image:: https://img.shields.io/travis/sunscrapers/django-getpaid.svg\n    :target: https://travis-ci.org/sunscrapers/django-getpaid\n.. image:: https://api.codacy.com/project/badge/Coverage/d25ba81e2e4740d6aac356f4ac90b16d\n    :target: https://www.codacy.com/manual/dekoza/django-getpaid\n.. image:: https://img.shields.io/pypi/wheel/django-getpaid.svg\n    :target: https://pypi.org/project/django-getpaid/\n.. image:: https://img.shields.io/pypi/l/django-getpaid.svg\n    :target: https://pypi.org/project/django-getpaid/\n.. image:: https://api.codacy.com/project/badge/Grade/d25ba81e2e4740d6aac356f4ac90b16d\n    :target: https://www.codacy.com/manual/dekoza/django-getpaid\n\n=============================\nWelcome to django-getpaid\n=============================\n\n\ndjango-getpaid is payment processing framework for Django\n\nDocumentation\n=============\n\nThe full documentation is at https://django-getpaid.readthedocs.io.\n\nFeatures\n========\n\n* support for multiple payment brokers at the same time\n* very flexible architecture\n* support for asynchronous status updates - both push and pull\n* support for modern REST-based broker APIs\n* support for multiple currencies (but one per payment)\n* support for global and per-plugin validators\n* easy customization with provided base abstract models and swappable mechanic (same as with Django\'s User model)\n\n\nQuickstart\n==========\n\nInstall django-getpaid and at least one payment backend:\n\n.. code-block:: console\n\n    pip install django-getpaid\n    pip install django-getpaid-payu\n\nAdd them to your ``INSTALLED_APPS``:\n\n.. code-block:: python\n\n    INSTALLED_APPS = [\n        ...\n        \'getpaid\',\n        \'getpaid_payu\',  # one of plugins\n        ...\n    ]\n\nAdd getpaid to URL patterns:\n\n.. code-block:: python\n\n    urlpatterns = [\n        ...\n        path(\'payments/\', include(\'getpaid.urls\')),\n        ...\n    ]\n\nDefine an ``Order`` model by subclassing ``getpaid.models.AbstractOrder``\nand define some required methods:\n\n.. code-block:: python\n\n    from getpaid.models import AbstractOrder\n\n    class MyCustomOrder(AbstractOrder):\n        amount = models.DecimalField(decimal_places=2, max_digits=8)\n        description = models.CharField(max_length=128)\n        buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)\n\n        def get_absolute_url(self):\n            return reverse(\'order-detail\', kwargs={"pk": self.pk})\n\n        def get_total_amount(self):\n            return self.amount\n\n        def get_buyer_info(self):\n            return {"email": self.buyer.email}\n\n        def get_currency(self):\n            return "EUR"\n\n        def get_description(self):\n            return self.description\n\n.. note:: If you already have an Order model and don\'t want to subclass ``AbstractOrder``\n    just make sure you implement all methods.\n\nInform getpaid of your Order model in ``settings.py`` and provide settings for payment backends:\n\n.. code-block:: python\n\n    GETPAID_ORDER_MODEL = \'yourapp.MyCustomOrder\'\n\n    GETPAID_BACKEND_SETTINGS = {\n        "getpaid_payu": {\n            # take these from your merchant panel:\n            "pos_id": 12345,\n            "second_key": "91ae651578c5b5aa93f2d38a9be8ce11",\n            "oauth_id": 12345,\n            "oauth_secret": "12f071174cb7eb79d4aac5bc2f07563f",\n        },\n    }\n\nWrite a view that will create the Payment.\n\nAn example view and its hookup to urls.py can look like this:\n\n.. code-block:: python\n\n    # orders/views.py\n    from getpaid.forms import PaymentMethodForm\n\n    class OrderView(DetailView):\n        model = Order\n\n        def get_context_data(self, **kwargs):\n            context = super(OrderView, self).get_context_data(**kwargs)\n            context["payment_form"] = PaymentMethodForm(\n                initial={"order": self.object, "currency": self.object.currency}\n            )\n            return context\n\n    # main urls.py\n\n    urlpatterns = [\n        # ...\n        path("order/<int:pk>/", OrderView.as_view(), name="order_detail"),\n    ]\n\nYou\'ll also need a template (``order_detail.html`` in this case) for this view.\nHere\'s the important part:\n\n.. code-block::\n\n    <h2>Choose payment broker:</h2>\n    <form action="{% url \'getpaid:create-payment\' %}" method="post">\n        {% csrf_token %}\n        {{ payment_form.as_p }}\n        <input type="submit" value="Checkout">\n    </form>\n\n\nRunning Tests\n=============\n\n.. code-block:: console\n\n    poetry install\n    poetry run tox\n\n\nAlternatives\n============\n\n* `django-payments <https://github.com/mirumee/django-payments>`_\n\n\nCredits\n=======\n\nCreated by `Krzysztof Dorosz <https://github.com/cypreess>`_.\nRedesigned and rewritten by `Dominik Kozaczko <https://github.com/dekoza>`_.\n\nProudly sponsored by `SUNSCRAPERS <http://sunscrapers.com/>`_\n\n\n\nDisclaimer\n==========\n\nThis project has nothing in common with `getpaid <http://code.google.com/p/getpaid/>`_ plone project.\n',
    'author': 'Dominik Kozaczko',
    'author_email': 'dominik@kozaczko.info',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/django-getpaid/django-getpaid',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
