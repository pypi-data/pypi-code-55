from setuptools import setup, find_packages

setup(
    name='Edatora',
    version='0.2',
    packages=find_packages(),
    license='MIT',
    description='A python package that runs exploratory data analysis for users',
    long_description=open('README.md').read(),
    install_requires=['pandas', 'matplotlib', 'seaborn', 'PySimpleGUI', 'sklearn', 'numpy', 'scipy', 'statsmodels', 'more-itertools', 'scikit-learn'],
    url='https://https://github.com/kianweelee/Edator',
    download_url= 'https://github.com/kianweelee/Edator/archive/0.2.tar.gz',
    author='Lee Kian Wee',
    author_email='leekianwee@outlook.com'
)