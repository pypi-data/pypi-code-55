import setuptools

with open("D:\\kaustik\\python_projects\\moosha\\moosha-ai_pypi\\README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Kaustik", # Replace with your own username
    version="0.0.1",
    author="kaustik",
    author_email="bhabburkaustik@gmail.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bhabburkaustik/moosha_ai/blob/master/moosha.py",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)