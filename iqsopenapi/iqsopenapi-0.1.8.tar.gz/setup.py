import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name="iqsopenapi",
    version="0.1.8",
    author="inquantstudio",
    author_email="sunliusi@hotmail.com",
    description="inquantstudio quant open api",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://www.inquantstudio.com/",
    packages=setuptools.find_packages(),
    install_requires=['pycryptodome>=3.7.2','websocket-client>=0.57.0',],
    package_data = {
        '': ['*.dll','*.so'],
    },
    classifiers=['Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",],)
