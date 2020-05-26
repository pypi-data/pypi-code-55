import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name='db_utils_ge',
    version='1.0.0',
    # scripts=['db_utils'],
    author='Oleg Osychenko',
    author_email="oleg.osychenko@ge.com",
    description="DB access helper utilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.build.ge.com/Fleet-Analytics-Europe/smart_mcr",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows"
    ],
)
