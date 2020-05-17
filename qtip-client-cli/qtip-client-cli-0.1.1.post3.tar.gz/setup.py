from setuptools import setup, find_packages

setup(
    name='qtip-client-cli',
    packages=find_packages('src'),
    author='Shubham Naik',
    author_email='shub@shub.club',
    url='https://github.com/4shub/qtip',
    version='0.1.1-rev3',
    package_dir={'': 'src', },
    install_requires=[
        'flask',
        'requests'
    ],
    entry_points= {
        "console_scripts": [
            "qtip = src.cli.qtip:main",
        ]
    },
    setup_requires=[
        'setuptools>=41.0.1',
    ]
)