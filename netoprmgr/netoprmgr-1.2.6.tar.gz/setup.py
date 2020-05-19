from setuptools import setup
from setuptools import find_packages





setup(
    name="netoprmgr",
    version="v1.2.6",
    description="Project to Manage Network Operation.",
    long_description="Project to Manage Network Operation.\nType 'python -m netoprmgr.__main__' to run program.\nNow using flask",
    #long_description_content_type="text/markdown",
    url="https://github.com/FunGuardian/netoprmgr",
    author="Funguardian, Dedar, Luthfi",
    author_email="cristiano.ramadhan@gmail.com",
    license="GPLv3+",
    packages=find_packages(exclude=("test*",)),
 
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3.6'
    ],
    include_package_data=True
)
