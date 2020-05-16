import setuptools

with open('README.md', 'r') as description_file:
    long_description = description_file.read()

setuptools.setup(
    name='pylocale',
    version='0.0.1',
    author='Cirill Usachov (Kyrylo Usachov)',
    author_email='mave7dev@gmail.com',
    description='A Python3 library without dependencies that provides'
                ' static translations across your app',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/mavedev/pylocale',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
