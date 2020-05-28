from setuptools import setup
from io import open

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pymetronome',
    version='0.1.0',
    packages=['met'],
    url='https://github.com/spyoungtech/pymetronome',
    license='MIT',
    author='Spencer Phillip Young',
    author_email='spencer.young@spyoung.com',
    description='A simple metronome utility',
    long_description=long_description,
    long_description_content_type='text/markdown',
    entry_points={
        'console_scripts': [
            'met = met.met:main'
        ]
    }
)
