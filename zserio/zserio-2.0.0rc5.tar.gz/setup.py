import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

required_url = []
required = []
with open("requirements.txt", "r") as freq:
    for line in freq.read().split():
        if "://" in line:
            required_url.append(line)
        else:
            required.append(line)

with open("current/zserio/version.txt", "r") as version_file:
    version = version_file.read().strip()

packages = setuptools.find_packages("current")

setuptools.setup(
    name="zserio",
    version=version,
    url="http://zserio.org",
    author="Navigation Data Standard e.V.",
    author_email="support@nds-association.org",

    description="Zserio runtime and Python package generator.",
    long_description=long_description,
    long_description_content_type="text/markdown",

    package_dir={'': 'current'},
    packages=packages,
    include_package_data=True,
    package_data={
        'zserio': ['zserio.jar']
    },

    install_requires=required,
    dependency_links=required_url,
    python_requires='>=3.6',

    license = "BSD-3 Clause",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: BSD License"
     ],
)
