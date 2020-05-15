
import setuptools

setuptools.setup(name='chromwindow',
      version='1.1.5',
      author="Kasper Munch",
      description='Utilities for working with windows on a chromosome.',
      # long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/kaspermunch/chromwindow',
      packages=setuptools.find_packages(),
      python_requires='>=3.6',
      install_requires=[
            'pandas>=1.0',
      ])

