try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

CLASSIFIERS=[
    'Development Status :: 4 - Beta',
    'License :: OSI Approved :: BSD License',
    'Framework :: Django',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Topic :: Internet :: WWW/HTTP',
]

setup(
    name='zipline-django-pyodbc-azure',
    version='1.9.12.2',
    description='Django backend for Microsoft SQL Server using pyodbc forked from django-pyodbc-azure',
    long_description=open('README.rst').read(),
    long_description_content_type='text/markdown',
    author='Neeraja',
    author_email='neeraja.anil2012@gmail.com',
    url='https://github.com/neerajaanil/zipline-django-pyodbc-azure',
    license='BSD',
    packages=['sql_server', 'sql_server.pyodbc'],
    install_requires=[
        'Django>=1.9.12,<1.10',
        'pyodbc>=3.0',
    ],
    classifiers=CLASSIFIERS,
    keywords='azure django',
)
