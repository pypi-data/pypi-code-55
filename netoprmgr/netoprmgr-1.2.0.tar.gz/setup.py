from setuptools import setup
from setuptools import find_packages





setup(
    name="netoprmgr",
    version="v1.2.0",
    description="Project to Manage Network Operation.",
    long_description="Project to Manage Network Operation.\nType 'python -m netoprmgr.__main__' to run program.\nNow using flask",
    #long_description_content_type="text/markdown",
    url="https://github.com/FunGuardian/netoprmgr",
    author="Funguardian, Dedar, Luthfi",
    author_email="cristiano.ramadhan@gmail.com",
    license="GPLv3+",
    packages=find_packages(exclude=("test*",)),
    install_requires=[
        'netmiko==3.1.0',
        'xlrd==1.2.0',
        'XlsxWriter==1.2.8',
        'python-docx==0.8.10',
        'Flask==1.1.2',
        'Flask-SQLAlchemy==2.4.1',
        'Flask-Bcrypt==0.7.1',
        'Flask-Login==0.5.0',
        'Flask-WTF==0.14.3',
    ],
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3.6'
    ),
    include_package_data=True
)
