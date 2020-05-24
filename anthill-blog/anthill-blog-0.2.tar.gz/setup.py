
from setuptools import setup, find_namespace_packages

DEPENDENCIES = [
    "anthill-common>=0.2.4"
]

setup(
    name='anthill-blog',
    package_data={
      "anthill.event": ["anthill/blog/sql", "anthill/blog/static"]
    },
    version='0.2',
    description='A service to deliver news and patch notes feed to the users inside the game',
    author='desertkun',
    license='MIT',
    author_email='desertkun@gmail.com',
    url='https://github.com/anthill-platform/anthill-blog',
    namespace_packages=["anthill"],
    include_package_data=True,
    packages=find_namespace_packages(include=["anthill.*"]),
    zip_safe=False,
    install_requires=DEPENDENCIES
)
