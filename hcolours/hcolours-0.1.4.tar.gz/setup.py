from setuptools import setup
with open("README.rst", "r") as fh:
    long_description = fh.read()
setup(
    name='hcolours',
    version='0.1.4',
    description='a colours package',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    packages=['hcolours'],
    author='Hs sH',
    author_email='spi0003@boxhillhs.vic.edu.au',
    keywords=['colours', 'hcolours', 'hs sh'],
    url='https://pypi.org/project/hcolours/#files'
)