import setuptools

def readme():
    with open("README.md", "r") as fh:
        long_description = fh.read()
    return long_description

setuptools.setup(
    name='db_conn',  
    version='1.0',
    description="Database connection (Postgres, Redshift)",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/oracy/db_conn",
    author="Oracy Martos",
    author_email="oramartos_21@hotmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Intended Audience :: Developers",
        "Topic :: Database",
        "Environment :: Console",
        "Operating System :: OS Independent",
    ],
    packages=['db_conn'] ,
    include_package_data=True,
    install_requires=["psycopg2"],
)
