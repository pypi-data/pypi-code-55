from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='besalu-notifier',
    author='Alex Schokking',
    author_email = "aschokking@gmail.com",
    license = "MIT",
    version='0.1.1',
    description='A tool to watch the inventory of Cafe Besalu in Seattle, WA.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aschokking/besalu-notifier",
    py_modules=['cli'],
    install_requires=[
        'Click',
        'notify-run'
    ],
    entry_points='''
        [console_scripts]
        besalu=cli:cli
    ''',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)