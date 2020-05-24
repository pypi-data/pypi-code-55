import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="yugiohdeck-api",
    version="0.0.1.dev7",
    author="gallantron",
    author_email="treeston.mmoc@gmail.com",
    description="Transforms yugiohdeck.github.io links into card data (and back)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://yugiohdeck.github.io/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['ygorganization-api'],
)