"micro-dict2json setup module."

def main():

    from setuptools import setup
    from dict2json import Dict2Json as d2j

    install_requires = ["microapp>=0.2.3"]

    setup(
        name=d2j._name_,
        version=d2j._version_,
        description=d2j._description_,
        long_description=d2j._long_description_,
        author=d2j._author_,
        author_email=d2j._author_email_,
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
        keywords="microapp dict2json",
        include_package_data=True,
        install_requires=install_requires,
        packages=["dict2json"],
        entry_points={"microapp.apps": "dict2json = dict2json"},
        project_urls={
            "Bug Reports": "https://github.com/grnydawn/micro-dict2json/issues",
            "Source": "https://github.com/grnydawn/micro-dict2json",
        }
    )

if __name__ == '__main__':
    import multiprocessing
    multiprocessing.freeze_support()
    main()
