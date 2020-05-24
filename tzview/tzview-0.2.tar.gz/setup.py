import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tzview",
    version="0.2",
    author="Julin S",
    author_email="julins@cannottellyou.yet",
    description="View datetime in different time zones.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ju-sh/tzview",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    classifiers=[
        # https://pypi.org/pypi?%3Aaction=list_classifiers
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Utilities",
        "Development Status :: 2 - Pre-Alpha",
        "Natural Language :: English",
    ],
    project_urls={
        'Changelog': 'https://github.com/ju-sh/tzview/CHANGELOG.md',
        'Issue Tracker': 'https://github.com/ju-sh/tzview/issues',
    },
    install_requires=['pytz', 'tzlocal'],
    python_requires='>=3.6',
)
