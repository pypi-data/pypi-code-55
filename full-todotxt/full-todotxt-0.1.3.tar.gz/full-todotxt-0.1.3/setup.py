import io
from setuptools import setup

requirements = [
    "todotxtio>=0.2.3",
    "dateparser>=0.7.4",
    "click>=7.1.2",
    "prompt-toolkit>=3.0.5"
]

# Use the README.md content for the long description:
with io.open('README.md', encoding='utf-8') as fo:
    long_description = fo.read()

setup(
    name='full-todotxt',
    version="0.1.3",
    url='https://github.com/seanbreckenridge/full_todotxt',
    author='Sean Breckenridge',
    author_email='seanbrecke@gmail.com',
    description=('''todotxt interactive interface that forces you to specify attributes'''),
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    test_suite='tests',
    py_modules=["full_todotxt"],
    install_requires=requirements,
    scripts=["full_todotxt"],
    keywords='todotxt todo.txt todo',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ],
)
