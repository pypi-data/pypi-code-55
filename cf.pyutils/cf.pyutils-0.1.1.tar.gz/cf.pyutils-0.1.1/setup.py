from setuptools import setup
import os

# if os.environ.get('CI_COMMIT_TAG'):
#     version = os.environ['CI_COMMIT_TAG']
# else:
#     version = os.environ['CI_JOB_ID']

setup(
    name="cf.pyutils",
    include_package_data=True,
    install_requires=[],
    version="0.1.1",
    url="https://gitlab.com/MatthieuJacquemet/pyutils",
    author="Matthieu Jacquemet",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
