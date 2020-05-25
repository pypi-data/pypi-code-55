"micro-nmlread setup module."

def main():

    from setuptools import setup
    from nmlread import NamelistReader as reader

    install_requires = ["microapp>=0.2.3", "f90nml"]

    setup(
        name=reader._name_,
        version=reader._version_,
        description=reader._description_,
        long_description=reader._long_description_,
        author=reader._author_,
        author_email=reader._author_email_,
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
        keywords="microapp nmlread",
        include_package_data=True,
        install_requires=install_requires,
        packages=["nmlread"],
        entry_points={"microapp.apps": "nmlread = nmlread"},
        project_urls={
            "Bug Reports": "https://github.com/grnydawn/micro-nmlread/issues",
            "Source": "https://github.com/grnydawn/micro-nmlread",
        }
    )

if __name__ == '__main__':
    import multiprocessing
    multiprocessing.freeze_support()
    main()
