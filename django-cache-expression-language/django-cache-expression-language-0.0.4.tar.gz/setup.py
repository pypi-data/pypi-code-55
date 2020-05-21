import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='django-cache-expression-language',
    version='0.0.4',
    author='Irsyad Rizaldi',
    author_email='irsyad.rizaldi97@gmail.com',
    description='Expression Language Cache Decorator for Django',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/dadangeuy/dcel',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Framework :: Django',
        'Environment :: Web Environment',
    ],
    python_requires='>=3',
)
