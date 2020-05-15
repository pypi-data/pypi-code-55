from setuptools import setup, find_namespace_packages
from os import path
from io import open

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='phiskills.grpc',  # Required
    version='0.0.1',  # Required
    description='Phi Skills Generic gRPC API Server',  # Optional
    long_description=long_description,  # Optional
    long_description_content_type='text/markdown',  # Optional
    url='https://github.com/phiskills/grpc-api.py',  # Optional
    author='Phi Skills',  # Optional
    author_email='hello@phiskills.com',  # Optional
    license='GNU GPLv3',  # Optional
    classifiers=[  # Optional
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development',
    ],
    keywords='Phi Skills gRPC API Server',  # Optional
    packages=find_namespace_packages(include=['phiskills.*']),  # Required
    python_requires='>=3.8, <4',
    install_requires=['grpcio', 'grpcio-health-checking'],  # Optional
    project_urls={  # Optional
        'Company website': 'https://phiskills.com',
        'Documentation': 'https://github.com/phiskills/grpc-api.py',
        'Source': 'https://github.com/phiskills/grpc-api.py',
    },
)
