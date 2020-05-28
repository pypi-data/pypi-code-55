from setuptools import setup


setup(
    name='Tri_Vail',
    version='0.1.0',
    py_modules=['Trail_Vail'],
    install_requires=[
        'Click', 'requests'
    ],
    entry_points= '''
    [console_scripts]
    RandAlgo=Trail_Vail:get_started
    ''',

) 