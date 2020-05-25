from setuptools import setup, find_packages


setup(
    name='red-dead-tools',
    version="0.1.2",
    packages=find_packages(),
    url="https://github.com/red-dead-tools/red-dead-tools",
    description="Tools for playing Red Dead Redemption 2 online",
    author="Tom Viner",
    author_email="red-dead-tools@viner.tv",
    install_requires=[
        'gspread',
        'attrs',
        'httpx',
        'decopatch',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
