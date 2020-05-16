import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="procspec",
    version="0.0.2",
    author="Sergiy Popovych",
    author_email="sergiy.popovich@gmail.com",
    description="Library for simple and powerful YAML specification of computational tasks.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/supersergiy/procspec",
    include_package_data=True,
    package_data={'': ['*.py']},
    install_requires=[
      'six',
    ],
    packages=setuptools.find_packages(),
)
