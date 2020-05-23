from setuptools import setup, find_packages


setup(
    name = 'my_names_P_T',
    version = '1.0.0',
    description = "Generate random names with lenght",
    long_description = 'long desct',
    long_description_content_type = 'text/markdown',
    url="",
    author = 'Przemek Tworkowski',
    author_email = 'po-tworek@o2.pl',
    include_package_data=True,
    keywords = 'random names',
    packages = find_packages(),
    scripts = ['my_names_pac/mynames.py', 'bin/gen_names.bat'],
    install_requires = ['names']
)