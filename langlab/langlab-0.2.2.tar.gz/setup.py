"langlab setup module."

def main():

    from setuptools import setup, find_packages
    from langlab.main import Langlab as llab

    console_scripts = ["langlab=langlab.__main__:main"]
    install_requires = ["microapp>=0.2.1"]

    setup(
        name=llab._name_,
        version=llab._version_,
        description=llab._description_,
        long_description=llab._long_description_,
        author=llab._author_,
        author_email=llab._author_email_,
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
        keywords="langlab",
        packages=find_packages(),
        include_package_data=True,
        install_requires=install_requires,
        entry_points={ "console_scripts": console_scripts,
            "microapp.projects": "langlab = langlab"},
        project_urls={
            "Bug Reports": "https://github.com/grnydawn/langlab/issues",
            "Source": "https://github.com/grnydawn/langlab",
        }
    )

if __name__ == '__main__':
    import multiprocessing
    multiprocessing.freeze_support()
    main()
