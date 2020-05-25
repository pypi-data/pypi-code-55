import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="volumio-websocket",
    version="1.0.7",
    description="Communicate with a volumio instance via websocket.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Heiss/volumio_websocket",
    author="Peter Heiss",
    author_email="peter.heiss@uni-muenster.de",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["volumio_websocket"],
    include_package_data=True,
    install_requires=["python-socketio[asyncio_client]"],
)