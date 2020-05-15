from setuptools import setup

with open('README.md', 'r') as f_desc:
    long_description = f_desc.read()

setup(
    name='exheader',
    version='0.0.1',
    description='Library for handling 3ds exheader files',
    long_description=long_description,
    long_description_content_type='text/markdown',
    py_modules=['exheader'],
    package_dir={'': 'src'},
    classifiers=[
        'Programming Language :: Python :: 3',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
