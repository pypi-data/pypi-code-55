import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nba_tracking_plotly", # Replace with your own username
    version="0.0.1.12",
    author="Avyay Varadarajan",
    author_email="avyayv@gmail.com",
    description="Plot nba tracking data using plotly",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/avyayv/nba_tracking_plotly",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)