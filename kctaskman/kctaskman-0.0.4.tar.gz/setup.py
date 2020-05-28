import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kctaskman",
    version="0.0.4",
    author="yinrong",
    author_email="yinrong@xiaomi.com",
    description="task manager",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git.n.xiaomi.com/bigdatakc/python-kctaskman/-/tree/master",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
