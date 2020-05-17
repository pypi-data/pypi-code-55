import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="django-emailuser",
    version="1.1.2",
    description="emailuser, make email as username, But unique username also exists.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Swe-HimelRana/django-email-user",
    author="Himel Rana",
    author_email="contact@himelrana-swe.com",
    license="MIT",
    keywords=['django', 'django emailuser', 'django email user',
              'django email username', 'django email as username'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
        "Framework :: Django",
        "Framework :: Django :: 2.0",
        "Framework :: Django :: 2.1",
        "Framework :: Django :: 2.2",
        "Framework :: Django :: 3.0",
    ],
    packages=["emailuser"],
    include_package_data=True,
    install_requires=['django',]

)
