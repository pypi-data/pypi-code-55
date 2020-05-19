import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

setuptools.setup(
    name='trackme',
    version='1.0.0',
    author='Bohdan Vey and Dmytro Lopushanskyy',
    description='Social media monitoring',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/DmytroLopushanskyy/Social-Media-Monitoring',
    packages=setuptools.find_packages(exclude=['examples']),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=required
)