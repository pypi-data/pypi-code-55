from setuptools import setup, find_packages

with open("README.md", encoding='utf-8') as fp:
    long_description = fp.read()

setup(
    name="django-material-icon-widget",
    version="0.1",
    license="MIT",
    description="Icon Picker for admin panel In Django",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Adi Eyal",
    author_email="adi@openup.org.za",
    url="https://github.com/adieyal/django-material-icon-widget",
    download_url="https://github.com/adieyal/django-material-icon-widget/archive/v0.1.tar.gz",  #<- should be changed 
    packages=find_packages(),
    keywords=["widget", "utility"],
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
