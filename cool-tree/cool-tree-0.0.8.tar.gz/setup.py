import io
from setuptools import setup, find_packages


# Read in the README for the long description on PyPI
def long_description():
    with io.open('README.md', 'r', encoding='utf-8') as f:
        readme = f.read()
    return readme


setup(name='cool-tree',
    version='0.0.8',
    url='https://github.com/Superb-AI-Suite/cool-tree.git',
    license='MIT',
    author='Superb AI',
    author_email='support@superb-ai.com',
    description='Suite Standard Library',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],
    packages=find_packages(exclude=['tests']),
    long_description=long_description(),
    long_description_content_type='text/markdown',
    install_requires=['requests', 'stringcase', 'python-datauri'],
    zip_safe=False
)
