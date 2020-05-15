import os
from setuptools import find_packages, setup
from asgiref_trio import __version__


# We use the README as the long_description
readme_path = os.path.join(os.path.dirname(__file__), "README.rst")


setup(
    name='asgiref-trio',
    version=__version__,
    url='http://github.com/django/asgiref/',
    author='Django Software Foundation',
    author_email='foundation@djangoproject.com',
    description='ASGI specs, helper code, and adapters',
    long_description=open(readme_path).read(),
    license='BSD',
    zip_safe=False,
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    extras_require={
        "tests": [
            "pytest~=4.3.0",
            "pytest-asyncio~=0.10.0",
        ],
    },
    install_requires=[],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
    ],
)
