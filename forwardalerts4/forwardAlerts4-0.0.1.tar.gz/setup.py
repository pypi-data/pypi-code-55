from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()


setup (
    name="forwardAlerts4",
    version="0.0.1",
    packages=["forwardAlert4"],
    author = "Ajayi Praise",
    author_email = "praiseajayi2@gmail.com",
    description = "A forum for fake job postings ",
    long_description =long_description,
    long_description_conten_type = "text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    include_package_data=True,
    install_requires=["twilio", "pyfiglet", "termcolor", ],
    entry_points={
        "console_scripts": [
            "forwardAlert4 = forwardAlert4.__main__:main",
        ]
    },

)