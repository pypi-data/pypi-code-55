# @Author: Anthony Walker <walkanth>
# @Date:   2020-02-28T08:20:49-08:00
# @Email:  dev.sokato@gmail.com
# @Last modified by:   walkanth
# @Last modified time: 2020-02-28T11:25:56-08:00



import setuptools

with open("README.md", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="enotipy", # Replace with your own username
    version="1.0.3",
    author="Anthony Walker",
    author_email="dev.notipy@gmail.com",
    license='BSD 3-clause "New" or "Revised License"',
    description="ENotipy is a package to wrap your code and email you upon it's completion",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/awa1k3r/Notipy",
    entry_points={
        'console_scripts': [
            'enotipy=enotipy.enotipy:lineRun'
        ]
    },
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
