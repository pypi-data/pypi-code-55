# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['walter']

package_data = \
{'': ['*']}

install_requires = \
['appdirs', 'attrs', 'begins']

setup_kwargs = {
    'name': 'walter',
    'version': '1.1',
    'description': 'A better configuration library for Django and other Python projects',
    'long_description': 'Walter\n======\n\nWalter is a configuration library, inspired by `python-decouple <https://pypi.python.org/pypi/python-decouple>`_, and intended to replace direct access to ``os.environ`` in Django ``settings.py`` files (although it is by no means Django-specific). It currently supports Python 3.6+.\n\nIt differs from other, similar libraries for one reason: when your users try to start up your app with invalid configuration, the error message they get shows a list of **all of the errors** with every configuration parameter, not just the first one.\n\nInstallation\n------------\n\n.. code-block:: shell\n\n    pip install walter\n    # or\n    poetry add walter\n\nUsage\n-----\n\nHere\'s an example of a Python file that uses Walter to define its configuration.\n\n::\n\n    from walter.config import Config\n\n    with Config("Acme Inc.", "My Awesome App") as config:\n\n        # Read a configuration value with config()\n        SECRET_KEY = config(\'SECRET_KEY\')\n\n        # Convert the returned value to something other than a string with cast.\n        DEBUG = config(\'DEBUG\', cast=bool)\n\n        # You can pass any function that takes a string to `cast`.\n        # Here, we\'re using a third party function to parse a database URL\n        # string into a Django-compatible dictionary.\n        import dj_database_url\n        DATABASES = {\n            \'default\': config(\'DATABASE_URL\', cast=dj_database_url.parse),\n        }\n\n        # You can also make a parameter optional by giving it a default.\n        SENTRY_DSN = config(\'SENTRY_DSN\', default=None)\n\n    print(f"Here, you can use values like {SITE_NAME}!")\n\nIf we run that code without setting anything, Walter throws an error at the end of the ``with`` block.\n\n.. code-block:: pytb\n\n    Traceback (most recent call last):\n    File "<stdin>", line 27, in <module>\n    File "/Users/leigh/Projects/walter/walter/config.py", line 90, in __exit__\n        raise ConfigErrors(errors=self.errors)\n    walter.config.ConfigErrors: 4 configuration values not set, 0 invalid\n\n    SECRET_KEY not set\n    DEBUG not set\n    DATABASE_URL not set\n    SITE_NAME not set\n\nNote that Walter lists out all of the errors in our configuration, not just the first one! If we set all of those settings as environment variables and run the code again, the code runs to completion:\n\n.. code-block:: text\n\n    Here, you can use values like MyAwesomeApp!\n',
    'author': 'Leigh Brenecki',
    'author_email': 'leigh@brenecki.id.au',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://walter.leigh.party',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>3.6',
}


setup(**setup_kwargs)
