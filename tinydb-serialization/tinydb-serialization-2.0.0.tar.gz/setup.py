# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tinydb_serialization']

package_data = \
{'': ['*']}

install_requires = \
['tinydb>=4.0,<5.0']

setup_kwargs = {
    'name': 'tinydb-serialization',
    'version': '2.0.0',
    'description': "Serialization for objects that TinyDB otherwise couldn't handle",
    'long_description': "tinydb-serialization\n^^^^^^^^^^^^^^^^^^^^\n\n|Build Status| |Coverage| |Version|\n\n``tinydb-serialization`` provides serialization for objects that TinyDB\notherwise couldn't handle.\n\nUsage\n*****\n\nCreating a Serializer\n---------------------\n\nIn this example we implement a serializer for ``datetime`` objects:\n\n.. code-block:: python\n\n    from datetime import datetime\n    from tinydb_serialization import Serializer\n\n    class DateTimeSerializer(Serializer):\n        OBJ_CLASS = datetime  # The class this serializer handles\n\n        def encode(self, obj):\n            return obj.strftime('%Y-%m-%dT%H:%M:%S')\n\n        def decode(self, s):\n            return datetime.strptime(s, '%Y-%m-%dT%H:%M:%S')\n\nUsing a Serializer\n------------------\n\nYou can use your serializer like this:\n\n.. code-block:: python\n\n    >>> from tinydb import TinyDB\n    >>> from tinydb_serialization import SerializationMiddleware\n    >>> from tinydb import Query\n    >>>\n    >>> from datetime import datetime\n    >>>\n    >>>\n    >>> serialization = SerializationMiddleware()\n    >>> serialization.register_serializer(DateTimeSerializer(), 'TinyDate')\n    >>>\n    >>> db = TinyDB('db.json', storage=serialization)\n    >>> db.insert({'date': datetime(2000, 1, 1, 12, 0, 0)})\n    >>> db.all()\n    [{'date': datetime.datetime(2000, 1, 1, 12, 0)}]\n    >>> query = Query()\n    >>> db.insert({'date': datetime(2010, 1, 1, 12, 0, 0)})\n    >>> db.search(query.date > datetime(2005, 1, 1))\n    [{'date': datetime.datetime(2010, 1, 1, 12, 0)}]\n\n\nFor a more complexe example that provides better time support, check out `issue #6 <https://github.com/msiemens/tinydb-serialization/issues/6>`_.\n\nChangelog\n*********\n\n**v2.0.0** (2020-05-26)\n-----------------------\n\n- Add TinyDB v4.0.0 support (see `pull request #9 <https://github.com/msiemens/tinydb-serialization/pull/9>`_)\n\n**v1.0.4** (2017-03-27)\n-----------------------\n\n- Don't modify the original element if it contains a list (see\n  `pull request #5 <https://github.com/msiemens/tinydb-serialization/pull/5>`_)\n\n**v1.0.3** (2016-02-11)\n-----------------------\n\n- Handle nested data (nested dicts, lists) properly when serializing/deserializing (see\n  `pull request #3 <https://github.com/msiemens/tinydb-serialization/pull/3>`_)\n\n**v1.0.2** (2016-01-04)\n-----------------------\n\n- Don't destroy original data when serializing (see\n  `pull request #2 <https://github.com/msiemens/tinydb-serialization/pull/2>`_)\n\n**v1.0.1** (2015-11-17)\n-----------------------\n\n- Fix installation via pip (see `issue #1 <https://github.com/msiemens/tinydb-serialization/issues/1>`_)\n\n**v1.0.0** (2015-09-27)\n-----------------------\n\n- Initial release on PyPI\n\n.. |Build Status| image:: https://img.shields.io/github/workflow/status/msiemens/tinydb-serialization/Python CI?style=flat-square\n   :target: https://github.com/msiemens/tinydb-serialization/actions?query=workflow%3A%22Python+CI%22\n.. |Coverage| image:: https://img.shields.io/coveralls/msiemens/tinydb-serialization.svg?style=flat-square\n   :target: https://coveralls.io/r/msiemens/tinydb-serialization\n.. |Version| image:: https://img.shields.io/pypi/v/tinydb-serialization.svg?style=flat-square\n   :target: https://pypi.python.org/pypi/tinydb-serialization/\n",
    'author': 'Markus Siemens',
    'author_email': 'markus@m-siemens.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
