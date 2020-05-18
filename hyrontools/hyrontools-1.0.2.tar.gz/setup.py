import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hyrontools",
    version="1.0.2",
    author="Jacob Neil Taylor",
    author_email="me@jacobtaylor.id.au",
    description="Hyron CLI Tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jacobneiltaylor/hyrontools",
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    package_data={
        "hyrontools": [
            "assets/*"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",  # noqa
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'hyrontools = hyrontools.__main__:main',
        ],
    },
    python_requires='>=3.7',
    install_requires=[
        "hyron",
        "boto3"
    ],
)
