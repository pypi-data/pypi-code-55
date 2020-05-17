from setuptools import setup

# reading long description from file
with open('DESCRIPTION.txt') as file:
    long_description = file.read()


# specify requirements of your package here
REQUIREMENTS = ['opencv-python', 'numpy', 'collections']

# some more details
CLASSIFIERS = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    ]

# calling the setup function 
setup(name='MMSICHE',
      version='1.0.3',
      description='Library that implements MMSICHE algorithm',
      long_description=long_description,
      url='https://github.com/abhinavbajpai2012/MMSICHE',
      author='Abhinav Bajpai',
      author_email='abhinavbajpai2012@gmail.com',
      license='MIT',
      packages=['MMSICHE'],
      classifiers=CLASSIFIERS,
      install_requires=REQUIREMENTS,
      keywords='Image Processing - MMSICHE',
	  python_requires='>=2.3',
      )
