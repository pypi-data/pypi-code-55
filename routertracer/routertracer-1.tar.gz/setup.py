import setuptools

import setuptools
#
# with open("README.md", "r") as fh:
#     long_description = fh.read()

setuptools.setup(
    name="routertracer", # Replace with your own username
    version="1",
    author="klauswong123",
    author_email="klauswangjinpeng@gmail.com",
    description="Output traceroute hops 'ip, rtt, AS number, and service provider' into a json file",
    # long_description=long_description,
    # long_description_content_type="text/markdown",
    url="https://github.com/klauswong123/routertracert",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)