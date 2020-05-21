from setuptools import setup
import pathlib

# The directory containing this file
HERE = pathlib.Path(__file__).parent

setup(name='pythonspell',
    version='1.2',
    description='A simple python spellchecker built on BK Trees and Damerau Levenshtein distance',
    url='https://github.com/AidanJSmith/Pythonspell',
    long_description_content_type="text/markdown",
    long_description="README.MD",
    author='Aidan Smith',
    author_email='100023755@mvla.net',
    license='MIT',
    keywords='spelling corrector autocorrect',
    packages=['pyspell'],
    zip_safe=False)