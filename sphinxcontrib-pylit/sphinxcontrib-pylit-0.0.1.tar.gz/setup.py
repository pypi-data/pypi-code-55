import os
from setuptools import setup

setup(
	name='sphinxcontrib-pylit',
      version='0.0.1',
      description='Literate Programming extension for Sphinx',
      url='https://github.com/rblack42/sphinxcontrib-pylit',
      author='Roie R. Black',
      author_email='roie.black@gmail.com',
      license='BSD',
      packages=['sphinxcontrib', os.path.join('sphinxcontrib', 'pylit')],
      zip_safe=False)
