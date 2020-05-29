import os
import setuptools
import sys

with open("yaz_messaging_plugin/version.py") as file:
    globals = {}
    exec(file.read(), globals)
    version = globals["__version__"]

if sys.argv[-1] == "tag":
    os.system("git tag -a {} -m \"Release {}\"".format(version, version))
    os.system("git push origin {}".format(version))
    sys.exit()

if sys.argv[-1] == "publish":
    os.system("python3 setup.py sdist upload")
    os.system("python3 setup.py bdist_wheel upload")
    sys.exit()

setuptools.setup(
    name="yaz_messaging_plugin",
    packages=["yaz_messaging_plugin"],
    version=version,
    description="A symfony message translation plugin for YAZ",
    author="Boudewijn Schoon",
    author_email="boudewijn@zicht.nl",
    url="http://github.com/yaz/yaz_messaging_plugin",
    license="MIT",
    zip_safe=False,
    install_requires=["yaz", "pyyaml", "googletrans"],
    scripts=["bin/yaz-messaging"],
    test_suite="nose.collector",
    tests_require=["nose"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6"
    ])
