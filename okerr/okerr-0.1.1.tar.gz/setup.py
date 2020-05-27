from setuptools import setup

readme = open('README.rst').read()

setup(
    name='okerr',
    version='0.1.1',
    description='A simple Result with match functionality for Python',
    author='Rafael Marques',
    author_email='rafaelomarques@gmail.com',
    url='https://github.com/ceb10n/okerr',
    packages=['okerr'],
    zip_safe=True,
    include_package_data=True,
    license='MIT',
    keywords='result match rust',
    long_description=readme,
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
    ],
    install_requires=[
        'typing; python_version < "3.5"'
    ],
    extras_require={
        'test': [
            'coverage',
            'flake8',
            'mock',
            'pylint',
            'pytest',
            'pytest-cov'
        ]
    }
)
