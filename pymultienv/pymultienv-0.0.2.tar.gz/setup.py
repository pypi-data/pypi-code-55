import setuptools

setuptools.setup(
    name='pymultienv',
    version='0.0.2',
    description='pymultienv is a command to help you deal with multiple python environments',
    long_description='this is the long description of pymultienv',
    url='https://veltzer.github.io/pymultienv',
    download_url='https://github.com/veltzer/pymultienv',
    author='Mark Veltzer',
    author_email='mark.veltzer@gmail.com',
    maintainer='Mark Veltzer',
    maintainer_email='mark.veltzer@gmail.com',
    license='MIT',
    platforms=['python3'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
    ],
    keywords='git python repositories multiple',
    packages=setuptools.find_packages(),
    install_requires=[
        'gitpython',
        'pyfakeuse',
    ],
    entry_points={
        'console_scripts': [
            'pymultienv=pymultienv.me:cli',
        ],
    },
)
