from setuptools import setup


def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name='RandAlgo_py',
    version='1.0.0',
    description='A python package to fetche random algorithm questions',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url="https://github.com/startng/Forward-RandAlgo-jaynwauche",
    author='Nwauche Junior Chimenka',
    author_email = 'juniornwauche@gmail.com',
    license='MIT',
    classifiers = [
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8'
    ],
    packages=['RandAlgo_py'],
    include_package_data = True,
    install_requires=['requests', 'bs4', 'lxml'],
    entry_points={
        'console_scripts': [
            'Randalgo_cli = RandAlgo_py.cli:main',
        ],
    }
)