from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='artisinal_integers',
      version='0.2.1',
      description='Get unique artisinal integers, locally sourced!',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='http://github.com/micahwalter/artisinal_integers',
      author='Micah Walter',
      author_email='micah@micahwalter.com',
      license='MIT',
      packages=['artisinal_integers'],
			install_requires=[
                          'requests',
                        ],
      zip_safe=False
)
