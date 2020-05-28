import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="text-actions-girvel",
    version="0.0.2",
    author="girvel",
    author_email="widauka@yandex.ru",
    description="Package for managing UI commands in text package in bash syntax",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/girvel/text_actions",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
