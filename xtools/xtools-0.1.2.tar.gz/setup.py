from setuptools import setup

setup(name="xtools",
      version="0.1.2",
      author="Baptiste Fontaine",
      author_email="b@ptistefontaine.fr",
      description="XTools API wrapper",
      long_description=open('README.md').read(),
      long_description_content_type='text/markdown',
      url="https://github.com/bfontaine/xtools",
      install_requires=['requests'],
      license="MIT",
      packages=['xtools'],
      # https://pypi.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Topic :: Software Development',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3 :: Only',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Operating System :: OS Independent',
      ])
