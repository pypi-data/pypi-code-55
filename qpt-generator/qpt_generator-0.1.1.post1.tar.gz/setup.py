from setuptools import setup, find_packages
from Cython.Build import cythonize

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name="qpt_generator",
      version="0.1.1.post1",
      description="Question Paper Template Generator",
      long_description=long_description,
      long_description_content_type='text/markdown',
      author="Niraj Kamdar",
      package_data={
          'qpt_generator': ["*.pxd", "*.pyx", "*.cpp", "*.h"]
      },
      packages=find_packages(),
      ext_modules=cythonize('qpt_generator/qpt_generator.pyx'),
      license='MIT',
      url='https://github.com/Niraj-Kamdar/qpt_generator',
      download_url='https://github.com/user/reponame/archive/v_01.tar.gz',
      keywords=['question', 'paper', 'template', 'generator'],
      install_requires=[
          'cython',
      ],
      classifiers=[
          'Development Status :: 3 - Alpha',
          # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
          'Intended Audience :: Developers',
          'Topic :: Software Development :: Build Tools',
          "Natural Language :: English",
          "Operating System :: OS Independent",
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
      ],
      )
