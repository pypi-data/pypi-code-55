import setuptools

print(setuptools.find_packages())

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='pywisc',
     version='0.74',
     license='MIT',
     author="Andres Vazquez",
     author_email="andres@data99.com.ar",
     description="Wisc calculations",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/cluster311/pywisc",
     install_requires=[
         'requests>=2.23.0'
     ],
     include_package_data=True,  
     packages=['pywisc'],  # setuptools.find_packages(),
     entry_points = {
        'console_scripts': [
            'wisc=pywisc.command_line:main'
            ],
     },
     classifiers=[
         'Programming Language :: Python :: 3',
         'Programming Language :: Python :: 3.6',
         'License :: OSI Approved :: MIT License',
         'Operating System :: OS Independent',
         'Intended Audience :: Developers', 
     ],
     python_requires='>=3.6',
 )