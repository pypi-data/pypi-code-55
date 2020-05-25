import setuptools

from wtforms_field_factory import __version__


with open("README.md", "r") as readme:
    setuptools.setup(
        name="wtforms-field-factory",
        version=__version__,
        author="v7a",
        long_description=readme.read(),
        long_description_content_type="text/markdown",
        url="https://github.com/v7a/wtforms-field-factory",
        keywords=["wtforms", "field", "factory", "on-the-fly"],
        install_requires=["wtforms >= 2.3"],
        py_modules=["wtforms_field_factory"],
        license="MIT",
        project_urls={
            "Source": "https://github.com/v7a/wtforms-field-factory",
            "Tracker": "https://github.com/v7a/wtforms-field-factory/issues",
        },
        classifiers=[
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Developers",
            "Programming Language :: Python :: 3 :: Only",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            "Topic :: Internet :: WWW/HTTP",
        ],
    )
