from setuptools import setup

setup(
    name='SpuhlLibrary',
    version='1.1.10',
    packages=['tests', 'tests.edgemessages', 'spuhllib', 'spuhllib.edgemessages', 'spuhllib.util'],
    url='https://github.com/sagerpascal/Spuhl_IoT_Solution',
    license='',
    author='Luca Staehli, Pascal Sager',
    author_email='pascal.sager@spuhl.com',
    description='Azure IoT Library from Spuhl GmbH',
    test_suite="tests",
    install_requires=['azure-iot-device~=2.1.1']

)