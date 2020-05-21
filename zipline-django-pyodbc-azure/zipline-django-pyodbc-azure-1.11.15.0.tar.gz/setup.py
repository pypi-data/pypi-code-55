try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

CLASSIFIERS=[
    'Development Status :: 4 - Beta',
    'License :: OSI Approved :: BSD License',
    'Framework :: Django',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Topic :: Internet :: WWW/HTTP',
]

setup(
    name='zipline-django-pyodbc-azure',
    version='1.11.15.0',
    description='Django backend for Microsoft SQL Server using pyodbc forked from django-pyodbc-azure',
    long_description=open('README.rst').read(),
    long_description_content_type='text/markdown',
    author='Michiya Takahashi , modified by Neeraja',
    author_email='neeraja.anil2012@gmail.com',
    url='https://github.com/neerajaanil/zipline-django-pyodbc-azure',
    license='BSD',
    packages=['sql_server', 'sql_server.pyodbc'],
    install_requires=[
        'Django>=1.11.15,<2.0',
        'pyodbc>=3.0',
    ],
    classifiers=CLASSIFIERS,
    keywords='azure django',
)
