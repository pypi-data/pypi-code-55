# Copyright © CZ.NIC, z. s. p. o.
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from setuptools import setup

with open("README.md", "r") as readme:
    long_description = readme.read()


def read_requirements(filename="requirements.txt"):
    def valid_line(line):
        line = line.strip()
        return line and not any(line.startswith(p) for p in ("#", "-"))

    def extract_requirement(line):
        egg_eq = "#egg="
        if egg_eq in line:
            _, requirement = line.split(egg_eq, 1)
            return requirement
        return line

    with open(filename) as f:
        lines = f.readlines()
        return list(map(extract_requirement, filter(valid_line, lines)))


setup(
    name="fenix-checker",
    use_scm_version=True,
    packages=["fenix_checker"],
    setup_requires=["setuptools_scm"],
    description="A small server which checks if user's IP is in a trusted Fenix network.",
    author="Jiri Helebrant",
    author_email="jiri.helebrant@nic.cz",
    url="https://gitlab.labs.nic.cz/websites/fenix-checker",
    install_requires=read_requirements(),
    keywords=["fenix"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.6",
    long_description=long_description,
    long_description_content_type="text/markdown"
)
