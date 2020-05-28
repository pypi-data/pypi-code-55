from setuptools import setup

setup(
    name="beancount_mnb",
    version="1.0.1-rc0",
    description="Az MNB hivatalos középárfolyamainak letöltését megvalósító beancount plugin.",
    keywords="beancount importer mnb currency",
    url="https://github.com/belidzs/beancount_mnb",
    author="Balázs Keresztury",
    license="MIT",
    packages=["beancount_mnb"],
    install_requires=[
        "beancount>=2.2.1",
        "zeep>=3.2.0",
        "pytz>=2018.9",
        "lxml>=4.3.2"
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: Plugins",
        "Natural Language :: Hungarian",
        "Topic :: Office/Business :: Financial :: Accounting"
    ],
    zip_safe=False)
