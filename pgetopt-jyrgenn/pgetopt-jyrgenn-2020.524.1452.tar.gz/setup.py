import os
import sys
import setuptools

with open("README.md", "r") as fh:
    # filter out the comment lines from the README
    description_lines = [ l for l in fh if not l.startswith("#") ]

setuptools.setup(
    name="pgetopt-jyrgenn",
    version=os.environ["PKG_VERSION"] or sys.exit("missing $PKG_VERSION env."),
    author="Juergen Nickelsen",
    author_email="ni@w21.org",
    description=description_lines[0].strip(),
    long_description="".join(description_lines),
    long_description_content_type="text/markdown",
    url="https://git.w21.org/python_modules/pgetopt",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
