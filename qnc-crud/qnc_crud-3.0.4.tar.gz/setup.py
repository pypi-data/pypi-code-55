import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="qnc_crud",
    version="3.0.4",
    author="Alex Fischer",
    author_email="alex@quadrant.net",
    description="A set of utilities/mini-frameworks for building CRUD apps with Django",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/quadrant-newmedia/qnc_crud",
    packages=['qnc_crud', 'qnc_crud.tests'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=["Django>=2.2,<3.1", "django_early_return>=0.0,<1"],
    include_package_data=True,
)