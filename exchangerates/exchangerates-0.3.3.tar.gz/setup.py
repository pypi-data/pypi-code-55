from setuptools import setup, find_packages


setup(
    name='exchangerates',
    version='0.3.3',
    description="A module to make it easier to handle historical exchange rates",
    long_description="",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Programming Language :: Python :: 3.6',
	'Programming Language :: Python :: 3.7'
    ],
    author='Mark Brough',
    author_email='mark@brough.io',
    url='http://github.com/markbrough/exchangerates',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'examples']),
    namespace_packages=[],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'lxml >= 4.4.0',
        'requests >= 2.22.0',
        'six >= 1.12.0'
    ],
    entry_points={
    }
)
