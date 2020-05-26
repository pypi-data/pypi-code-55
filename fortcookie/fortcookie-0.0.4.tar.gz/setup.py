import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fortcookie", # Replace with your own username
    version="0.0.4",
    author="Rafael Stoffalette Joao",
    author_email="rafaelstojoao@gmail.com",
    description="Say cookie.crack() and be lucky...",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rafaelstojoao/fortcookie",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
