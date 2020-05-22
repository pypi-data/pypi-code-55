"uxml2dict setup module."

def main():

    from setuptools import setup
    from uxml2dict import Xml2Dict as x2d

    install_requires = ["microapp>=0.2.1", "xmltodict"]

    setup(
        name=x2d._name_,
        version=x2d._version_,
        description=x2d._description_,
        long_description=x2d._long_description_,
        author=x2d._author_,
        author_email=x2d._author_email_,
        classifiers=[
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Science/Research",
            "Topic :: Scientific/Engineering",
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.5",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
        ],
        keywords="microapp uxml2dict",
        include_package_data=True,
        install_requires=install_requires,
        packages=["uxml2dict"],
        entry_points={"microapp.apps": "uxml2dict = uxml2dict"},
        project_urls={
            "Bug Reports": "https://github.com/grnydawn/uxml2dict/issues",
            "Source": "https://github.com/grnydawn/uxml2dict",
        }
    )

if __name__ == '__main__':
    import multiprocessing
    multiprocessing.freeze_support()
    main()
