from setuptools import setup

setup(
    name='portmanpy',
    version='0.0.0',    
    description='Portfolio Management for Jupyter',
    url='https://github.com/genarionogueira/portmanpy',
    author='Genario Nogueira',
    author_email='genarionogueira2@gmail.com',
    license='BSD 2-clause',
    packages=['portmanpy'],
    install_requires=['pandas'],

    classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: BSD License',  
        'Programming Language :: Python :: 3',
    ],
)