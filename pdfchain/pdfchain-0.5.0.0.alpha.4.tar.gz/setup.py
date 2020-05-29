#!/usr/bin/env python3

import os
# import sys
import setuptools


def get_data_files():
    data_files = []

    for path, dirs, files in os.walk("share"):
        # target_path = os.path.join("/usr", path)
        # target_path = os.path.join(sys.prefix, path)
        target_path = path
        data_files.append((target_path, [os.path.join(path, f) for f in files]))
    print("data_files: '{}'".format(data_files)) #TEST
    return data_files


def main():
    with open("README.md", "r") as fh:
        long_description = fh.read()

    setuptools.setup(
        name = "pdfchain",
        version = "0.5.0.0 alpha 4",
        author = "Martin Singer",
        author_email = "martin.singer@web.de",
        description = "A graphical user interface for the PDF Toolkit",
        long_description = long_description,
        long_description_content_type = "text/markdown",
        keywords = "PDF",
        url = "https://pdfchain.sourceforge.io/",
        download_url = "https://sourceforge.net/p/pdfchain/neo/ci/master/tree/",
        license='GPLv3+',
        # package_dir = {"": "src"},
        packages = setuptools.find_packages(),
        data_files = get_data_files(),
        # scripts = ["bin/pdfchain"],
        entry_points = {"gui_scripts": ["pdfchain = pdfchain.__main__:main"]},
        classifiers = [
            "Development Status :: 3 - Alpha",
            "Environment :: X11 Applications :: GTK",
            "Intended Audience :: End Users/Desktop",
            "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
            "Operating System :: POSIX",
            "Topic :: Office/Business",
            "Programming Language :: Python :: 3",
        ],
        python_requires = ">=3.6",
        # install_requires = ["PyGObject"],
    )


if __name__ == "__main__":
    main()
