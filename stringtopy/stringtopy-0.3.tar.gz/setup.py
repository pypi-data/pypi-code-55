import setuptools

import versioneer

#DESCRIPTION_FILES = ["pypi-intro.rst"]
#
#long_description = []
#import codecs
#for filename in DESCRIPTION_FILES:
#    with codecs.open(filename, 'r', 'utf-8') as f:
#        long_description.append(f.read())
#long_description = "\n".join(long_description)


setuptools.setup(
    name = "stringtopy",
    version = versioneer.get_version(),
    packages = setuptools.find_packages(),
    install_requires = [],
    author = "James Tocknell",
    author_email = "aragilar@gmail.com",
    description = "stringtopy is a small library to convert strings to a specified type (e.g. int, float or bool), allowing more human friendly input similar to configparser.",
    #long_description = long_description,
    license = "3-clause BSD",
    keywords = "strings",
    url = "http://stringtopy.rtfd.io",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    cmdclass=versioneer.get_cmdclass(),
)
