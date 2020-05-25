
from setuptools import setup, find_packages


setup(name='raster2tiles',
      version='0.1.0',
      packages=find_packages(),
      python_requires='>=3',
      setup_requires=['Cython>=0.25.2', 'numpy>=1.13.1'],
      install_requires=[
        'cycler>=0.10.0',
        'decorator>=4.1.2',
        'enum34>=1.1.6',
        'GDAL==2.2.1',
        'numpy>=1.13.1',
        'olefile>=0.44',
        'pexpect>=4.2.1',
        'pickleshare>=0.7.4',
        'Pillow>=4.2.1',
        'prompt-toolkit>=1.0.15',
        'psycopg2>=2.7.3.1',
        'ptyprocess>=0.5.2',
        'Pygments>=2.2.0',
        'pyparsing>=2.2.0',
        'python-dateutil>=2.6.1',
        'pytz>=2017.2',
        'scandir>=1.5',
        'scipy>=0.19.1',
        'simplegeneric>=0.8.1',
        'six>=1.10.0',
        'SQLAlchemy>=1.2.0b2',
        'traitlets>=4.3.2',
        'wcwidth>=0.1.7'
      ],
      entry_points='''
        [console_scripts]
        raster2tiles=raster2tiles.cli:go
      ''',
      zip_safe=False)
