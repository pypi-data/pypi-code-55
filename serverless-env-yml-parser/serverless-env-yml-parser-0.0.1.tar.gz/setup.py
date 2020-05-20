from setuptools import setup, find_packages
import os

current_folder = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(current_folder, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='serverless-env-yml-parser',
    version='0.0.1',
    description='A package to extract environmental variables from serverless.env.yml for local development',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/endrus/sls-env-yml-parser',
    author='Andrei Khrapavitski',
    author_email='andrei.khrapavitski@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='serverless, sls, serverless.env.yml',
    packages=find_packages(exclude='tests'),
    python_requires='>=3.6',
    project_urls={
        'Documentation': r'https://github.com/endrus/sls-env-yml-parser'
    },
)