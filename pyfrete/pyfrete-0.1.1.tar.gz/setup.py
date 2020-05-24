from setuptools import setup

setup(
    name='pyfrete',
    version='0.1.1',    
    description='API for Brazillian Shipping Methods in Python',
    url='https://github.com/felipevisu/pyfrete',
    author='Felipe Faria',
    author_email='felipevisu@gmail.com',
    license='BSD 2-clause',
    packages=['pyfrete'],
    install_requires=['zeep>=3', 'zipp>=3'],

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],

    python_requires='>=3.6',
)