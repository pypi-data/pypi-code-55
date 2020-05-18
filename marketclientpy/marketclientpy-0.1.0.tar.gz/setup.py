from setuptools import setup

setup(
    name='marketclientpy',
    version='0.1.0',    
    description='Dowload free financial data',
    url='https://github.com/genarionogueira/marketClient',
    author='Genario Nogueira',
    author_email='genarionogueira2@gmail.com',
    license='MIT',
    packages=['marketclientpy'],
    install_requires=['pandas',
                      'datetime',                     
                      ],

    classifiers=[
        'Programming Language :: Python :: 3',        
    ],
)