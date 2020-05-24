import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

setup(
    name='django-pg-colorfield',
    version='1.0',
    description='A ColorField to save and filter by radius Colors in RGB array in postgresql.',
    long_description=README,
    url='https://gitlab.com/nayan32biswas/django-pg-colorfield',
    author='Nayan Biswas',
    author_email='nayan32biswas@gmail.com',
    license='MIT License',  # example license
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    # install_requires = ['django'],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)