from setuptools import setup
from os.path import join


with open('README.md') as readme_file:
    readme = readme_file.read()

with open(join('ratter', 'version.py')) as version_file:
    lines = version_file.readlines()
    metadict = dict()

    for line in lines:
        try:
            k, v = line.split('=')
            metadict.update({k.strip(): v.strip().strip('"')})
        except ValueError:
            pass

setup(
    name=metadict['__name__'],
    version=metadict['__version__'],
    author=metadict['__author__'],
    author_email=metadict['__email__'],
    description=metadict['__summary__'],
    url=metadict['__url__'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3 :: Only'
    ],
    long_description=readme,
    long_description_content_type='text/markdown'
)
