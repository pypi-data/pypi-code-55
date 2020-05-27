# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gsrest', 'gsrest.core', 'gsrest.elements', 'gsrest.helper', 'gsrest.xml']

package_data = \
{'': ['*']}

install_requires = \
['pyyaml>=5.3.1,<6.0.0']

setup_kwargs = {
    'name': 'gsrest',
    'version': '0.1.3',
    'description': 'GeoServer python REST API client',
    'long_description': '# gsrest\n\nGeoServer python REST API client.\n\n## About\n\nThis package is on an early stage, but may be functional for your needs.\n\nAt this point, the only documentation is the one on source files and the tests\nthemself.\n\n## Features\n\n  * HTTP only. *Warning*: your geoserver credentials may be publicly exposed.\n  * Python >= 3.7.\n  * Static setup of the connection for all GeoServer elements.\n  * Easily extendable.\n  * Support to load elements from a YAML file.\n  * Just PyYAML as runtime dependency.\n\n## Installation\n\n```\npip install gsrest\n```\n\n## Sample usage\n\nTo test the client, you need a geoserver instance. For simplicity, in this\nexample we will use the [geoserver docker image from\nkartoza](https://hub.docker.com/r/kartoza/geoserver/):\n\n```\n$ docker run -d --rm -p 8080:8080 --name geoserver kartoza/geoserver:2.17.0\n```\n\nLet\'s setup the client credentials. Default values work fine with the docker\ninstance.\n\n```\n$ python\n>>> from gsrest import client\n>>> client.GsClient()  # will setup the connection for all elements\n```\n\nNext, let\'s create a local workspace and sync (upload) it to the server.\n\n```\n>>> from gsrest.elements import workspace\n>>> wsp = workspace.WorkSpace("wsp1")\n>>> wsp.uri = "http://my.uri/"\n>>> wsp.sync()\n```\n\nThen, you can check the new workspace at http://localhost:8080/geoserver\n(user `admin` / password `geoserver`).\n\nFinally, do not forget to kill the docker instance.\n\n```\n$ docker kill geoserver\n```\n\n## License\n\nLicensed under the term of `GPL-3.0-or-later LICENSE`. See [LICENSE](LICENSE).\n',
    'author': 'Eduardo Suarez-Santana',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/esuarezsantana/gsrest',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
