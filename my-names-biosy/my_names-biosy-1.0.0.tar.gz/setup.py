from setuptools import setup, find_packages

setup(
    name='my_names-biosy',
    version='1.0.0',
    description="Generate random names with lenght",
    long_description='long desct',
    long_description_content_type = 'text/markdown',
    url=" ",
    author='Lukasz Chalinski',
    author_email='l.chalinski@gmail.com',
    include_package_data=True,
    keywords='random names',
    packages=find_packages(),
    scripts=['my_names_pac/my_names.py', 'bin/my_names.bat'],
    install_requires=['names']
)
