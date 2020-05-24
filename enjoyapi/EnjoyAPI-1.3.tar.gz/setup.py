
from setuptools import setup



from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='EnjoyAPI',
    packages=['EnjoyAPI'],
    version='1.3',
    description='Ассинхронный клиент для API EnjoyMickeyBot',
    author='Kotypey',
    author_email='Kotypey@gmail.com',
    install_requires=['aiohttp', 'discord'],
    url="https://github.com/KotypeyPyEdition/EnjoyAPI",
    long_description=long_description,
    long_description_content_type='text/markdown'
)