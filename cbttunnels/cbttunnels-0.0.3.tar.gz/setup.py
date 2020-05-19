import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cbttunnels",
    version="0.0.3",
    author="CrossBrowserTesting",
    author_email="info@crossbrowsertesting.com",
    description="A wrapper for cbttunnels, to make testing local sites easier in CrossBrowserTesting",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/crossbrowsertesting/cbt_tunnels_py",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6.2',
    install_requires=["requests"]
)