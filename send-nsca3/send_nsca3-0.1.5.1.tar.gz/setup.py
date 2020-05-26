try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name="send_nsca3",
    version="0.1.5.1",
    author="gitmstoute",
    author_email="",
    url="https://github.com/gitmstoute/send_nsca3",
    description='python3 compatible pure-python nsca sender',
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)",
        "Topic :: System :: Monitoring",
        "Intended Audience :: Developers",
        "Development Status :: 4 - Beta",
    ],
    license="GNU Lesser General Public License v2 (LGPLv2)",
    scripts=["bin/py_send_nsca3"],
    packages=["send_nsca3"],
    provides=["send_nsca3"],
    install_requires=["pycrypto>=2.0.0", 'six'],
    tests_require=["nose", "mock==1.0.1"],
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown'
)
