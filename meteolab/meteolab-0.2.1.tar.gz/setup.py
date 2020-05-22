"meteolab setup module."

def main():

    from setuptools import setup
    from meteolab.main import Meteolab as mlab

    console_scripts = ["meteolab=meteolab.__main__:main"]
    install_requires = ["microapp>=0.2.1"]

    setup(
        name=mlab._name_,
        version=mlab._version_,
        description=mlab._description_,
        long_description=mlab._long_description_,
        author=mlab._author_,
        author_email=mlab._author_email_,
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
        keywords="meteolab",
        packages=[ "meteolab" ],
        include_package_data=True,
        install_requires=install_requires,
        entry_points={ "console_scripts": console_scripts,
            "microapp.projects": "meteolab = meteolab"},
        project_urls={
            "Bug Reports": "https://github.com/grnydawn/meteolab/issues",
            "Source": "https://github.com/grnydawn/meteolab",
        }
    )

if __name__ == '__main__':
    import multiprocessing
    multiprocessing.freeze_support()
    main()
