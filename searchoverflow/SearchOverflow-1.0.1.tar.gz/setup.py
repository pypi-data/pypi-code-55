from setuptools import setup, find_packages 
  
with open('requirements.txt') as f: 
    requirements = f.readlines() 
  
long_description = 'Python script to quickly look up questions on StackOverflow from the command line' 
  
setup( 
        name ='SearchOverflow', 
        version ='1.0.1', 
        author ='Airam Hernández Rocha', 
        author_email ='airamhr7@gmail.com', 
        url ='https://aiherroc.upv.edu.es', 
        description ='Script to make searches on StackOverflow', 
        long_description = long_description, 
        long_description_content_type ="text/markdown", 
        license ='Apache License 2.0', 
        packages = find_packages(), 
        entry_points ={ 
            'console_scripts': [ 
                'sflow = SearchOverflow.__init__:main'
            ] 
        }, 
        classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        ],
        keywords ='StackOverflow code search python java stackoverflow', 
        install_requires = requirements, 
        zip_safe = False
) 
