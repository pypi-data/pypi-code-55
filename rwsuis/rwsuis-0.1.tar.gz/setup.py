import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rwsuis",
    version="0.1",
    author="Ole Christian Handegård",
    author_email="ole.hande98@gmail.com",
    description="Python functions for ABB IRB-140",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/prinsWindy/ABB-Robot-Machine-Vision",
    packages=setuptools.find_packages(),
    install_requires=[
        'requests',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)