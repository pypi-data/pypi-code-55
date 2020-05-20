from setuptools import setup

setup(
    name='gemfeed',
    version='1.1.0',
    description="Atom feed generating tool for Gemini.",
    author="Solderpunk",
    author_email="solderpunk@sdf.org",
    url='https://tildegit.org/solderpunk/gemfeed',
    py_modules = ["gemfeed"],
    entry_points={
        "console_scripts": ["gemfeed=gemfeed:main"]
    },
    install_requires=["feedgen"],
)
