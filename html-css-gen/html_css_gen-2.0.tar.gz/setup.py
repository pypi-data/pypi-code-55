
import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='html_css_gen',
    version='2.0',
    author="guangyong",
    author_email="guangyong@live.com",
    description="snippet to merge html/css files",
    long_description=long_description,
    url="https://bitbucket.org/guangyong/html_css_gen/",
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
    ],
)
