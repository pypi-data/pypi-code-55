__version__ = '1.0.56'

import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(name='fes',
                 version=__version__,
                 author='Altertech',
                 author_email='div@altertech.com',
                 description='',
                 long_description=long_description,
                 long_description_content_type='text/markdown',
                 url='https://www.altertech.com/products/fes/',
                 packages=setuptools.find_packages(),
                 license='Propietary',
                 install_requires=[
                     'rapidtables==0.1.10', 'python-dateutil==2.7.3',
                     'neotermcolor==2.0.7', 'requests==2.23.0',
                     'cachetools==3.1.1', 'flask==1.1.1', 'sqlalchemy==1.3.10',
                     'psycopg2==2.8.4', 'pyaltt2==0.0.90', 'pyyaml==3.13',
                     'gunicorn==20.0.4', 'python-dateutil==2.7.3',
                     'jsonschema==2.6.0', 'finac==0.5.0'
                 ],
                 scripts=['bin/fes-control'],
                 classifiers=('Programming Language :: Python :: 3',))
