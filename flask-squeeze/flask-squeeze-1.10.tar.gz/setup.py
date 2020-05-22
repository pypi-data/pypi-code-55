# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flask_squeeze']

package_data = \
{'': ['*']}

install_requires = \
['brotli>=1.0.7,<2.0.0',
 'flask>=1.1.2,<2.0.0',
 'rcssmin>=1.0.6,<2.0.0',
 'rjsmin>=1.1.0,<2.0.0']

setup_kwargs = {
    'name': 'flask-squeeze',
    'version': '1.10',
    'description': 'Compress and minify Flask responses!',
    'long_description': '# Flask-Squeeze\n\n[![Downloads](https://pepy.tech/badge/flask-squeeze)](https://pepy.tech/project/flask-squeeze)\n[![Downloads](https://pepy.tech/badge/flask-squeeze/month)](https://pepy.tech/project/flask-squeeze/month)\n[![Downloads](https://pepy.tech/badge/flask-squeeze/week)](https://pepy.tech/project/flask-squeeze/week)\n\nFlask-Squeeze is a Flask extension that automatically:\n- Minifies JS and CSS responses.\n- Compresses all HTTP responses with brotli.\n- Caches static files so that they don\'t have to be re-compressed. The cache will be cleared each time Flask restarts! Files are considered to be static if they are contained in a directory that is named "static" (Or generally, if they contain "/static/" in their request path.\n\n## Installation\n```\npip3 install Flask-Squeeze\n```\n\n## Usage\n```python\nfrom flask_squeeze import Squeeze\nsqueeze = Squeeze()\n\n# Initialize Extension\nsqueeze.init_app(app)\n```\n\nThats all!\n\n## Options\nYou can configure Flask-Squeeze with the following options in your Flask config:\n- `COMPRESS_FLAG (default=True)`: Globally enables or disables Flask-Squeeze\n- `COMPRESS_MIN_SIZE (default=500)`: Defines the minimum file size in bytes to activate the brotli compression\n- `COMPRESS_LEVEL_STATIC (default=11)`: Possible value are 0 (lowest) to 11 (highest). Defines the compression level of brotli for files in static folders. Theses files fill also be cached, so that they only have to be compressed once.\n- `COMPRESS_LEVEL_DYNAMIC (default=5)`: Possible value are 0 (lowest) to 11 (highest). Defines the compression level of brotli for dynamic files like generated HTML files. Theses files will not be cached, so they will be compressed for each response.\n- `COMPRESS_MINIFY_CSS (default=True)`: Enable or disable css minification using rcssmin.\n- `COMPRESS_MINIFY_JS (default=True)`: Enable or disable css minification using rcssmin.\n\n- `COMPRESS_VERBOSE_LOGGING (default=False)`: Enable or disable verbose logging. If enabled, Flask-Squeeze will print what it does into the terminal in a highlighted color.\n',
    'author': 'Marcel Kröker',
    'author_email': 'kroeker.marcel@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
