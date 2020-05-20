import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django_cli_big2tinydev",
    version="0.0.4",
    author="Big2TinyDev",
    author_email="big2tinydev@gmail.com",
    description="A command line package that creates a Django project and app using your filesystem templates",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/big2tinydev/django_cli.git",
    packages=setuptools.find_packages(),
    install_requires=['django'],
    entry_points={
        'concole_scripts': [
            'newdjango = django_cli.create_new_project:main'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',

)