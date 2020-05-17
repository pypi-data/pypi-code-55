from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as readme_file:
    readme = readme_file.read()

requirements = ['beautifulsoup4>=4.9.0',]

setup_requirements = [ ]

test_requirements = [ ]

setup(
    author="milucp",
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description='pretty-print of html',
    entry_points={
        'console_scripts': [
            'xpprint=xpprint.cli:main',
        ],
    },
    install_requires=requirements,
    license="Apache Software License 2.0",
    include_package_data=True,
    keywords='xpprint',
    name='xpprint',
    packages=find_packages(include=['xpprint', 'xpprint.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/milucp/xpprint',
    version='0.1.5.1',
    zip_safe=False,
)
