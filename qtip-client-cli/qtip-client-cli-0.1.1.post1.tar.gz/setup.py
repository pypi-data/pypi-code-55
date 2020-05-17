from setuptools import setup, find_packages

setup(
    name='qtip-client-cli',
    packages=find_packages('src/cli'),
    author='Shubham Naik',
    author_email='shub@shub.club',
    url='https://github.com/4shub/qtip',
    version='0.1.1-rev1',
    package_dir={'': 'src/cli', },
    install_requires=[
        'flask',
        'requests'
    ],
    entry_points= {
        "console_scripts": [
            "qtip = qtip:main",
        ]
    },
    setup_requires=[
        'setuptools>=41.0.1',
    ]
)