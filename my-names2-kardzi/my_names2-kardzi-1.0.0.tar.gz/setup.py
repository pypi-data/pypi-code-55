from setuptools import setup, find_packages


setup(
    name = 'my_names2-kardzi',
    version = '1.0.0',
    description = "Generate random names with lenght",
    long_description = 'long desct',
    long_description_content_type = 'text/markdown',
    url="https://gitlab.com/Karolina_D",
    author = 'Karolina_D',
    author_email = 'dzilinska.karolina@gmail.com',
    include_package_data=True,
    keywords = 'random names',
    packages = find_packages(),
    scripts = ['my_names2/my_names2.py', 'bin/my_names2.bat'],
    install_requires = ['names']
)