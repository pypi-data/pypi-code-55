import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mysqlcp",
    version="1.0.0",
    author="AlaBouali",
    author_email="trap.leader.123@gmail.com",
    description="Simple, secure and advanced module to perform safe MySQL queries",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AlaBouali/mysqlcp",
    python_requires=">=2.7",
    install_requires=['pymysql'],
    packages=["mysqlcp"],
    license="MIT License",
    entry_points={
       'console_scripts': [
           'xmysql = mysqlcp.__main__:run',
       ],
    },
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License ",
    ],
)
