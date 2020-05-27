"""
Setup.py for Moss
"""
import os
import sys
import setuptools



uname = sys.platform.lower()
if os.name == 'nt':
    uname = 'win'
if uname.startswith('linux'):
    uname = 'linux'

# Dependencies: required and recommended modules
# do not use `install_requires` for conda environments
install_reqs = ['scipy>=1.2',
                'numpy>=1.12',
                'matplotlib>=3.0',
                'lmfit>=1.0',
                'uncertainties>=3.1',
                'pyshortcuts>=1.7',
                'pyqt>=5.9']


package_data = ['*.svg', '*.ico']


pjoin = os.path.join

bindir = 'bin'
pyexe = pjoin(bindir, 'python')
larchbin = 'larch'

if uname == 'win':
    bindir = 'Scripts'
    pyexe = 'python.exe'


setuptools.setup(
    name='mossba',
    version='0.1.1dev',
    author='C. Prestipino',
    author_email='cprest6@univ-univ-rennes1.fr',
    url='https://github.com/Prestipino/Moss',
    license='LICENSE.txt',
    description='Fit mossbauer',
    long_description=open('README.txt').read(),
    packages=setuptools.find_packages(),
    package_data={'Moss': package_data},
    entry_points={'console_scripts': ['Moss = Moss.MossGui:MossLauncher']},
    install_requires=install_reqs,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
