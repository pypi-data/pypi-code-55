from setuptools import setup,find_packages

setup(

    name='mpython_conn',
    version='0.1',
    keywords=('pip','mpython'),
    description="control mpython board by pc",
    long_description="control mpython board by pc via usb",
    licence='MIT Licence',

    url='https://github.com/jim0575/desktop-tutorial',
    author='james',
    author_email="jim0575@qq.com",

    packages=find_packages(),
    include_package_data=True,
    platforms='any',
    install_requires=['pySerial']
    )
