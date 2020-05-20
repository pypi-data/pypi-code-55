from setuptools import setup, find_packages

setup(
    name             = 'pymarktex',
    version          = '1.3.6',
    description      = 'Will convert a markdown text file to a fancy PDF document',
    long_description = open('README.md').read(),
    long_description_content_type = 'text/markdown',
    license          = 'MIT',
    url              = 'http://github.com/xapple/pymarktex/',
    author           = 'Lucas Sinclair',
    author_email     = 'lucas.sinclair@me.com',
    packages         = find_packages(),
    scripts          = ['scripts/pymarktex'],
    install_requires = ['autopaths>=1.3.8', 'plumbing>=2.7.3', 'pystache>=0.5.4'],
)