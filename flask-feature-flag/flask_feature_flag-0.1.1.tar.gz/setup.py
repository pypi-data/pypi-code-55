import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="flask_feature_flag",
    version="0.1.1",
    author="Terminus",
    author_email="jose.salas@zinobe.com",
    description="Flask feature flag",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/terminus-zinobe/flask-feature-flag",
    packages=setuptools.find_packages(
        exclude=["*.tests", "*.tests.*", "tests.*", "tests"]
    ),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'flask>=1.1.1',
        'flask-mongoengine>=0.9.5',
        'Flask-Caching>=1.8.0',
        'constants-and-utils>=0.0.1'
    ]
)
