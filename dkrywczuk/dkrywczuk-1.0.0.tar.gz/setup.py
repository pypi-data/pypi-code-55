from setuptools import setup, find_packages


setup(
    name = 'dkrywczuk',
    version = '1.0.0',
    description = "Generate random names with lenght",
    long_description = 'long desct',
    long_description_content_type = 'text/markdown',
    url=" ",
    author = 'Damian Krywczuk',
    author_email = 'methanoli@gmail.com',
    include_package_data=True,
    keywords = 'random names',
    packages = find_packages(),
    scripts = ['my_names2_pac/my_names2.py', 'bin/my_names2.bat'],
    install_requires = ['names']
)