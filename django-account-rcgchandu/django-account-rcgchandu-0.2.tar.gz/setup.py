import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()

setup(
    name='django-account-rcgchandu',
    version='0.2',
    packages=['account'],
    description='Simple authentication and registration for django apps',
    long_description=README,
    author='RCGCHANDU',
    author_email='ravichandravirgo@gmail.com',
    url='https://github.com/rcgchandu/django-account/',
    license='MIT',
    install_requires=[
        'Django>=1.6,<=3.0.6',
    ]
)