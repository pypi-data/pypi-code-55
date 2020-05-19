# M Tafaquh Fiddin Al Islami 2020
# TieF AI Tafaquh Fiddin Al Islami Library
# Author: M Tafaquh Fiddin Al Islami
#
# License: MIT


from distutils.core import setup
import setuptools

setup(
  name = 'tief',         # How you named your package folder (MyLib)
  packages = setuptools.find_packages(),   # Chose the same as "name"
  version = '0.1.9',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'TIEF.ai is an AI library for research and study purpose. This library is very easy to use. If you found some lack of performance or some issues, just tell me. I ll upgrade it as soon as possible.',   # Give a short description about your library
  author = 'M Tafaquh Fiddin Al Islami',                   # Type in your name
  author_email = 'tafaquh.fiddinal@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/tafaquh/tief',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/tafaquh/tief/archive/0.1.9.tar.gz',    # I explain this later on
  keywords = ['AI', 'Machine Learning', 'TIEF', 'Library'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
    'numpy',
    'pandas',
  ],
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
  python_requires='>=3.6',
)
