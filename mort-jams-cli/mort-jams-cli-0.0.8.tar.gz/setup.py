from __future__ import unicode_literals

import pathlib
from setuptools import setup, find_packages

# TODO: remove this when ready to publish official package
stealth_package_name = "mort-jams-cli"
stealth_author = "Ianois Olpxe"
stealth_description = "Smaet Ygiderp"


def setup_package():
    package_name = "prodigyteams"
    root = pathlib.Path(__file__).parent.resolve()

    # Read in package meta from about.py
    about_path = root / package_name / "about.py"
    with about_path.open("r", encoding="utf8") as f:
        about = {}
        exec(f.read(), about)

    # Read in requirements and split into packages and URLs
    requirements_path = root / "requirements.txt"
    with requirements_path.open("r", encoding="utf8") as f:
        requirements = [line.strip() for line in f]

    setup(
        name=stealth_package_name or package_name,
        description=stealth_description or about["__summary__"],
        author=stealth_author or about["__author__"],
        author_email=about["__email__"],
        url=about["__uri__"],
        version=about["__version__"],
        license=about["__license__"],
        packages=find_packages(),
        package_data={package_name: ["data/"]},
        install_requires=requirements,
        include_package_data=True,
        entry_points="""
            [console_scripts]
            ptc=prodigyteams.main:cli
        """,
    )


if __name__ == "__main__":
    setup_package()
