from setuptools import setup

setup(
    name="practicedatasets",
    version="0.3",
    description="Practice Dataset",
    long_description="This package contains different datasets like covid and world population. These datasets can be imported and acccessed as pandas dataframe or numpy array",
    long_description_content_type="text/x-rst",
    url="https://github.com/mehtarjt/practicedatasets",
    author="Rajat Mehta",
    author_email="mehtarjt@gmail.com",
    license="MIT",
    packages=["practicedatasets"],
    zip_safe=False,
    include_package_data=True,
)
