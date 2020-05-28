import setuptools

setuptools.setup(
    name = 'give_name_TP',
    version = '1.0.0',
    description = "Generate random names + their lenght",
    long_description = 'long desct',
    long_description_content_type = 'text/markdown',
    nclude_package_data=True,
    keywords = 'random names',
    packages = setuptools.find_packages(),
    scripts = ['my_names2_pac/my_names.py', 'bin/my_names.bat'],
    install_requires = ['names']
)
