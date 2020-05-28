from distutils.core import setup
from setuptools import setup,setuptools
import os 
with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme_file:
    readme = readme_file.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='nishanth',
    version='1.4',
    packages=setuptools.find_packages(),
    include_package_data=True,
    long_description_content_type= 'text/markdown',
    long_description=open('README.md').read(),
    description = "Tribute to Nishanth",
    author = "Vishnu Varthan Rao",
    author_email="vishnulatha006@gmail.com",
    install_requires=[
        "requests"
    ],
    license="MIT License",
    zip_safe=False,
    keywords='nishanth',
     classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
    ],

)

 #pypi-AgEIcHlwaS5vcmcCJDAwYzU2MmE1LTE0ZDEtNDhmYS1hZDZjLThlMTdlMjI3ZjQ4NQACJXsicGVybWlzc2lvbnMiOiAidXNlciIsICJ2ZXJzaW9uIjogMX0AAAYgJR2L70n7dCo5xSBKp5AgIJycuKhO3g2uSMvB6-gVqY8