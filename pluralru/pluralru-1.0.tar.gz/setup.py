from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="pluralru",
    version="1.0",
    description="Возвращает строку с множественным числом",
    long_description=readme(),
    long_description_content_type="text/markdown",
    author="Blazzerrr",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["pluralru"],
    include_package_data=True,
)

 
