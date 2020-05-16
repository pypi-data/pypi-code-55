from __future__ import absolute_import

from setuptools import find_packages, setup

with open('./README.md', 'r') as f:
    readme = f.read()


setup(
    name='github-automation',
    version='0.0.1',
    license='MIT',
    author_email='',
    description='GitHub automatic project manager tool',
    install_requires=[
    ],
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    long_description=readme,
    long_description_content_type='text/markdown',
    python_requires=">=3.7",
    classifiers=[
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ]
)
