import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="currency_api",
    version="0.0.1",
    author="Matthew Vasseur",
    author_email="mvasseur22@students.hopkins.edu",
    description="Gets current dollar values",
    long_description=long_description,
    long_description_content_type="text",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    package_data={
        "": ["*.txt", "*.rst", "*.json"],
        }
)
