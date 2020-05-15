from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="soc",
    version="0.0.1",
    packages=find_packages(),
    install_requires=["websockets==8.1"],
    author="Julian Nash",
    author_email="julianjamesnash@gmail.com",
    description="A lightweight websocket micro framework",
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords="websocket micro framework",
    url="https://github.com/Julian-Nash/soc",
    project_urls={
        "Bug Tracker": "https://github.com/Julian-Nash/soc",
        "Documentation": "https://github.com/Julian-Nash/soc",
        "Source Code": "https://github.com/Julian-Nash/soc",
    },
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
