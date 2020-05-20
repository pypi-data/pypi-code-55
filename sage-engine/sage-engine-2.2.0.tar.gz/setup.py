# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['sage',
 'sage.cli',
 'sage.database',
 'sage.database.core',
 'sage.database.hdt',
 'sage.database.postgres',
 'sage.database.statefull',
 'sage.grpc',
 'sage.http_server',
 'sage.query_engine',
 'sage.query_engine.iterators',
 'sage.query_engine.optimizer',
 'sage.query_engine.protobuf',
 'sage.query_engine.update']

package_data = \
{'': ['*'], 'sage.http_server': ['templates/*']}

install_requires = \
['PyYAML==5.1.2',
 'click==7.0',
 'fastapi==0.44.1',
 'grpcio>=1.26,<2.0',
 'protobuf==3.11.0',
 'rdflib-jsonld==0.4.0',
 'rdflib==4.2.2',
 'uvicorn==0.10.8',
 'uvloop==0.14.0']

extras_require = \
{'hdt': ['pybind11==2.2.4', 'hdt==2.3'], 'postgres': ['psycopg2-binary==2.7.7']}

entry_points = \
{'console_scripts': ['sage = sage.cli.http_server:start_sage_server',
                     'sage-grpc = sage.cli.grpc_server:start_grpc_server',
                     'sage-postgres-index = sage.cli.postgres:index_postgres',
                     'sage-postgres-init = sage.cli.postgres:init_postgres',
                     'sage-postgres-put = sage.cli.postgres:put_postgres']}

setup_kwargs = {
    'name': 'sage-engine',
    'version': '2.2.0',
    'description': 'Sage: a SPARQL query engine for public Linked Data providers',
    'long_description': '# Sage: a SPARQL query engine for public Linked Data providers\n[![Build Status](https://travis-ci.com/sage-org/sage-engine.svg?branch=master)](https://travis-ci.com/sage-org/sage-engine) [![PyPI version](https://badge.fury.io/py/sage-engine.svg)](https://badge.fury.io/py/sage-engine) [![Docs](https://img.shields.io/badge/docs-passing-brightgreen)](https://sage-org.github.io/sage-engine/)\n\n[Read the online documentation](https://sage-org.github.io/sage-engine/)\n\nSaGe is a SPARQL query engine for public Linked Data providers that implements *Web preemption*. The SPARQL engine includes a smart Sage client\nand a Sage SPARQL query server hosting RDF datasets (hosted using [HDT](http://www.rdfhdt.org/)).\nThis repository contains the **Python implementation of the SaGe SPARQL query server**.\n\nSPARQL queries are suspended by the web server after a fixed quantum of time and resumed upon client request. Using Web preemption, Sage ensures stable response times for query execution and completeness of results under high load.\n\nThe complete approach and experimental results are available in a Research paper accepted at The Web Conference 2019, [available here](https://hal.archives-ouvertes.fr/hal-02017155/document). *Thomas Minier, Hala Skaf-Molli and Pascal Molli. "SaGe: Web Preemption for Public SPARQL Query services" in Proceedings of the 2019 World Wide Web Conference (WWW\'19), San Francisco, USA, May 13-17, 2019*.\n\nWe appreciate your feedback/comments/questions to be sent to our [mailing list](mailto:sage@univ-nantes.fr) or [our issue tracker on github](https://github.com/sage-org/sage-engine/issues).\n\n# Table of contents\n\n* [Installation](#installation)\n* [Getting started](#getting-started)\n  * [Server configuration](#server-configuration)\n  * [Starting the server](#starting-the-server)\n* [Sage Docker image](#sage-docker-image)\n* [Command line utilities](#command-line-utilities)\n* [Documentation](#documentation)\n\n# Installation\n\nInstallation in a [virtualenv](https://virtualenv.pypa.io/en/stable/) is **strongly advised!**\n\nRequirements:\n* Python 3.7 (*or higher*)\n* [pip](https://pip.pypa.io/en/stable/)\n* **gcc/clang** with **c++11 support**\n* **Python Development headers**\n> You should have the `Python.h` header available on your system.   \n> For example, for Python 3.6, install the `python3.6-dev` package on Debian/Ubuntu systems.\n\n## Installation using pip\n\nThe core engine of the SaGe SPARQL query server with [HDT](http://www.rdfhdt.org/) as a backend can be installed as follows:\n```bash\npip install sage-engine[hdt,postgres]\n```\nThe SaGe query engine uses various **backends** to load RDF datasets.\nThe various backends available are installed as extras dependencies. The above command install both the HDT and PostgreSQL backends.\n\n## Manual Installation using poetry\n\nThe SaGe SPARQL query server can also be manually installed using the [poetry](https://github.com/sdispater/poetry) dependency manager.\n```bash\ngit clone https://github.com/sage-org/sage-engine\ncd sage-engine\npoetry install --extras "hdt postgres"\n```\nAs with pip, the various SaGe backends are installed as extras dependencies, using the  `--extras` flag.\n\n# Getting started\n\n## Server configuration\n\nA Sage server is configured using a configuration file in [YAML syntax](http://yaml.org/).\nYou will find below a minimal working example of such configuration file.\nA full example is available [in the `config_examples/` directory](https://github.com/sage-org/sage-engine/blob/master/config_examples/example.yaml)\n\n```yaml\nname: SaGe Test server\nmaintainer: Chuck Norris\nquota: 75\nmax_results: 2000\ngraphs:\n-\n  name: dbpedia\n  uri: http://example.org/dbpedia\n  description: DBPedia\n  backend: hdt-file\n  file: datasets/dbpedia.2016.hdt\n```\n\nThe `quota` and `max_results` fields are used to set the maximum time quantum and the maximum number of results\nallowed per request, respectively.\n\nEach entry in the `datasets` field declare a RDF dataset with a name, description, backend and options specific to this backend.\nCurrently, **only** the `hdt-file` backend is supported, which allow a Sage server to load RDF datasets from [HDT files](http://www.rdfhdt.org/). Sage uses [pyHDT](https://github.com/Callidon/pyHDT) to load and query HDT files.\n\n## Starting the server\n\nThe `sage` executable, installed alongside the Sage server, allows to easily start a Sage server from a configuration file using [Gunicorn](http://gunicorn.org/), a Python WSGI HTTP Server.\n\n```bash\n# launch Sage server with 4 workers on port 8000\nsage my_config.yaml -w 4 -p 8000\n```\n\nThe full usage of the `sage` executable is detailed below:\n```\nUsage: sage [OPTIONS] CONFIG\n\n  Launch the Sage server using the CONFIG configuration file\n\nOptions:\n  -p, --port INTEGER              The port to bind  [default: 8000]\n  -w, --workers INTEGER           The number of server workers  [default: 4]\n  --log-level [debug|info|warning|error]\n                                  The granularity of log outputs  [default:\n                                  info]\n  --help                          Show this message and exit.\n```\n\n# SaGe Docker image\n\nThe Sage server is also available through a [Docker image](https://hub.docker.com/r/callidon/sage/).\nIn order to use it, do not forget to [mount in the container](https://docs.docker.com/storage/volumes/) the directory that contains you configuration file and your datasets.\n\n```bash\ndocker pull callidon/sage\ndocker run -v path/to/config-file:/opt/data/ -p 8000:8000 callidon/sage sage /opt/data/config.yaml -w 4 -p 8000\n```\n\n# Documentation\n\nTo generate the documentation, navigate in the `docs` directory and generate the documentation\n\n```bash\ncd docs/\nmake html\nopen build/html/index.html\n```\n\nCopyright 2017-2019 - [GDD Team](https://sites.google.com/site/gddlina/), [LS2N](https://www.ls2n.fr/?lang=en), [University of Nantes](http://www.univ-nantes.fr/)\n',
    'author': 'Thomas Minier',
    'author_email': 'tminier01@gmail.com',
    'url': 'https://github.com/sage-org/sage-engine',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
