from setuptools import setup

setup(
    name='tcrhelloworld',
    version='0.1.2',
    description='simples example in the python world',
    url='',
    author='TheCloudRecipes',
    author_email='thecloudrecipes@gmail.com',
    license='MIT',
    packages=['tcrhelloworld'],
    zip_safe=False,
    entry_points = {
        'console_scripts': ['helloworld=tcrhelloworld.__main__:main'],
    }
)
