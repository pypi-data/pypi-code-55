from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='os-release',
    version='1.0',
    packages=['os_release'],

    author="Adam Zegelin",
    author_email="adam@zegelin.com",

    description="A module for reading systemd's os-release information on modern Linux distributions.",
    long_description=long_description,
    long_description_content_type="text/markdown",

    url="https://github.com/zegelin/py-os-release",

    install_requires=['arpeggio'],
    extras_require={
        'docs': ['sphinx', 'sphinx_autodoc_typehints', 'sphinx_paramlinks', 'sphinx_rtd_theme']
    },

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Database',
    ]
)