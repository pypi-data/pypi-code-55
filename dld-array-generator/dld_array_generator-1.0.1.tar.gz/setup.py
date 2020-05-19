# from distutils.core import setup

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

# setup(
#   name = 'DLD-Array-Generator',         # How you named your package folder (MyLib)
#   packages = ['DLD-Array-Generator'],   # Chose the same as "name"
#   version = '1.0.4',      # Start with a small number and increase it with every change you make
#   license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
#   description = 'Python package to generate parameterized DLD arrays.',   # Give a short description about your library
#   long_description = long_description,
#   long_description_content_type="text/markdown",
#   author = 'Morten Kals',                   # Type in your name
#   author_email = 'dev@mkals.no',      # Type in your E-Mail
#   url = 'https://github.com/mkals/DLD-Array-Generator',   # Provide either the link to your github or to your website
#   download_url = 'https://github.com/mkals/DLD-Array-Generator/archive/1.0.tar.gz',    # I explain this later on
#   keywords = ['DLD-array', 'dxf', 'microfluidics', 'filtering', 'size exclusion'],   # Keywords that define your package best
#   install_requires=[            # I get to this in a second
#           'numpy',
#           'ezdxf',
#       ],
#   classifiers=[
#     'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
#     'Intended Audience :: Developers',      # Define that your audience are developers
#     'Topic :: Software Development :: Build Tools',
#     'License :: OSI Approved :: MIT License',   # Again, pick a license
#     'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
#     'Programming Language :: Python :: 3.4',
#     'Programming Language :: Python :: 3.5',
#     'Programming Language :: Python :: 3.6',
#   ],
# )

setuptools.setup(
    name="dld_array_generator", # Replace with your own username
    version="1.0.1",
    author="Morten Kals",
    author_email="dev@mkals.no",
    description="Python package to generate parameterized DLD arrays.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mkals/dld_array_generator",
    packages=setuptools.find_packages(),
    install_requires=['numpy', 'ezdxf'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
