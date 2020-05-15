from setuptools import setup

setup(
    name='tg_tools',
    version='0.0.6',
    description='Standard toolset for development in TestGilde projects currently to simplify Config and MongoDB handling within docker container.',
    py_modules=['tg_tools'],
    package_dir={'': 'src'},
    install_requires=[
        'flask_pymongo',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
