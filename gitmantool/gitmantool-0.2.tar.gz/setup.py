import setuptools
from gitmanager.version import get_version

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gitmantool", # Replace with your own username
    version=str(get_version()),
    author='katmai',  # Optional
    author_email='katmai.mobil@gmail.com',  # Optional
    description='Console tool for manage projects on github/gitlab',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/katmai1/gitmanager",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3.6',
    entry_points={  # Optional
        'console_scripts': [
            'gm=gitmanager:main',
        ],
    },
    install_requires=[
        'docopt', 'pygithub', 'gitlab'
    ],
)
