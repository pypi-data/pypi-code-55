from setuptools import setup

with open("README.md", "r") as file_handler:
    long_description = file_handler.read()

setup(
    name='easy-ansi-widgets',
    version='0.0.0',
    url='https://gitlab.com/joeysbytes/easy-ansi-widgets',
    license='MIT',
    author='Joey Rockhold',
    author_email='joey@joeysbytes.net',
    description='Widgets made from the easy-ansi framework',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development",
        "Topic :: Terminals"
    ],
    python_requires='>=3.6'
)
