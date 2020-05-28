from setuptools import setup


def readme():
    with open('Readme.md') as f:
        readMe = f.read()
    return readMe


setup(
    name='Tri_Vail',
    version='0.1.1',
    description = ' A python package to display random trivia questions and answers',
    long_description=readme(),
    py_modules=['Trail_Vail'],
    install_requires=[
        'Click', 'requests'
    ],
    entry_points='''
    [console_scripts]
    RandAlgo=Trail_Vail:get_started
    ''',

)
