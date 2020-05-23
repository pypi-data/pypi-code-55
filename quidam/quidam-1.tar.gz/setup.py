# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


setup(
    name='quidam',
    version="1",
    packages=find_packages(),
    author="megadose",
    install_requires=["requests","json","fake_useragent","evolut","argparse"],
    description="Permet de recupérer des informations grace a la fonctionne mot de passe oubliée de certain sites",
    long_description="",
    include_package_data=True,
    url='http://github.com/megadose/Quidam',
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)
