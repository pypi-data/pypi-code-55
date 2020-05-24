import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='bet365',
    version='0.0.1',
    author="William Batista",
    author_email="ninja25538@tutanota.de",
    description="An odds scraper for Bet365 using Selenium and BeautifulSoup4",
    long_description=long_description,
    long_description_content_type="text/markdown",
    scripts=['scrape'],
    url="https://github.com/billyb2/bet365-scraper",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: Microsoft :: Windows :: Windows 10",
    ],
)
