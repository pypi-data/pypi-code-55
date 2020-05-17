from setuptools import setup, find_packages

print(find_packages('qtip-client-cli'))
setup(
    name='qtip-client-cli',
    packages=find_packages('qtip-client-cli'),
    py_modules=['qtip'],
    author='Shubham Naik',
    author_email='shub@shub.club',
    url='https://github.com/4shub/qtip',
    version='0.1.1-rev5',
    package_dir={'': 'qtip-client-cli' },
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