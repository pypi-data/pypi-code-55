#!/usr/scripts/env python

from distutils.core import setup

version = "1.0.3"

setup(name="m4db_database",
      version=version,
      license="MIT",
      description="M4DB database specification and utiltiles",
      url="https://bitbucket.org/micromag/m4db_database/src/master/",
      download_url="https://bitbucket.org/micromag/m4db_database/get/m4db_database-{}.zip".format(version),
      keywords=["micromagnetics", "database"],
      install_requires=["SQLAlchemy",
                        "pandas",
                        "PyYAML",
                        "Deprecated"],
      author="L. Nagy, W. Williams",
      author_email="lnagy2@ed.ac.uk",
      packages=["m4db_database"],
      package_dir={"m4db_database": "lib/m4db_database"},
      scripts=[
            "scripts/m4db_setup_database",
            "scripts/m4db_import_data"
      ],
      classifiers=[
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Developers",
            "Topic :: Database",
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
      ]),
