import setuptools

with open("README.md", "r") as fh:

    long_description = fh.read()

setuptools.setup(

     name='GenuineAI',

     version='0.0.1',

     author="Ernest (Khashayar) Namdar",

     author_email="ernest.namdar@utoronto.ca",

     description="Genuine AI functions used in iMICS Lab research projects",

     long_description=long_description,

     long_description_content_type = "text/markdown",

     packages=setuptools.find_packages(),

     classifiers=[

         "Programming Language :: Python :: 3",

         "License :: OSI Approved :: MIT License",

         "Operating System :: OS Independent",

     ],

 )
