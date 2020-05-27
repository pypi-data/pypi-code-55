from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='ccm_java8',
    version='1.0',
    py_modules=['ccm_java8'],

    author="Adam Zegelin",
    author_email="adam@instaclustr.com",

    description="CCM extension that starts Cassandra (and related tools) under Java 8",
    long_description=long_description,
    long_description_content_type="text/markdown",

    url="https://github.com/instaclustr/ccm-java8",

    install_requires=['ccm', 'os-release'],

    entry_points={
        'ccm_extension': ['java_home = ccm_java8:set_java_env']
    },

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: Plugins',
        'Environment :: MacOS X',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Database',
    ]
)