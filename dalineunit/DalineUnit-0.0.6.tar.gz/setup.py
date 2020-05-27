import setuptools

with open("readme.md", "r",encoding='utf8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="DalineUnit",
    version="0.0.6",
    author="kun.z",
    author_email="kun.z@daline.com.cn",
    description="daline unit generator and runner",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DalineWH",
    packages=['DalineUnit'],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords='daline Unit',
    install_requires=[

    ],
)

# python setup.py sdist bdist_wheel
# twine upload dist/*

