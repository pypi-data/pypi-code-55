import setuptools

setuptools.setup(
    name="internetgeminiserver",
    version="0.1.0",
    url="https://git.sr.ht/~martijnbraam/igs",
    license="MIT",
    author="Martijn Braam",
    author_email="martijn@brixit.nl",
    description="An multi-domain gemini server",
    py_modules=["igs"],
    entry_points={
        "console_scripts": [
            "igs=igs:main",
        ]
    },
    python_requires=">=3.7",
    keywords="gemini server tcp asyncio",
    classifiers=[
        "Environment :: Web Environment",
    ],
)
