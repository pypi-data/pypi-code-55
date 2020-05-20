
import setuptools

setuptools.setup(
     name='dokrtmp',
     version='0.0.1',
     scripts=['dokr'] ,
     author="Mirco Parschau",
     author_email="mirco.parschau@yahoo.com",
     description="A Docker and AWS utility package",
   long_description_content_type="text/markdown",
     url="https://github.com",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )
