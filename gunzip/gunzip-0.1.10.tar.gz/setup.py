"micro-gunzip setup module."

def main():

    from setuptools import setup
    from gunzip import Gunzip

    install_requires = ["microapp>=0.2.3"]

    setup(
        name=Gunzip._name_,
        version=Gunzip._version_,
        description=Gunzip._description_,
        long_description=Gunzip._long_description_,
        author=Gunzip._author_,
        author_email=Gunzip._author_email_,
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
        keywords="microapp gunzip",
        packages=["gunzip"],
        include_package_data=True,
        install_requires=install_requires,
        entry_points={"microapp.apps": "gunzip = gunzip"},
        project_urls={
            "Bug Reports": "https://github.com/grnydawn/micro-gunzip/issues",
            "Source": "https://github.com/grnydawn/micro-gunzip",
        }
    )

if __name__ == '__main__':
    import multiprocessing
    multiprocessing.freeze_support()
    main()
