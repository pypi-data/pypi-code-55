# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['serpent_image']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.18,<1.19',
 'pillow>=7.1,<7.2',
 'scikit-image>=0.17.1,<0.18.0',
 'scikit-learn>=0.22,<0.23']

setup_kwargs = {
    'name': 'serpentai-image',
    'version': '0.1.0',
    'description': 'Image class for Serpent.AI projects',
    'long_description': '# SerpentAI-Image\n\nImage class shared by multiple Serpent.AI Projects. Built on top of _NumPy_, _Pillow_, _scikit-image_ and _scikit-learn_.',
    'author': 'Nicholas Brochu',
    'author_email': 'nicholas@serpent.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://serpent.ai',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
