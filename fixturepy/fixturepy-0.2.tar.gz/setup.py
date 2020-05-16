from setuptools import setup

with open('README.md', 'r') as fh:
    long_description = fh.read()

test_dependencies = ['assertpy', 'email-validator']

setup(
    name='fixturepy',
    packages=['fixturepy'],
    version='0.2',
    license='MIT',
    description='Create random data to be used in tests',
    author='Exentrique Solutions',
    author_email='rs@exentriquesolutions.com',
    url='https://github.com/exentriquesolutions/fixturepy',
    keywords=['UnitTest', 'Fixture'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[],
    tests_require=test_dependencies,
    test_suite='tests',
    extras_require={
        'test': test_dependencies
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing :: Unit',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
