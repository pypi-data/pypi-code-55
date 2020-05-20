from setuptools import find_packages, setup
import pathlib

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(name='Growtopia',
      version='0.2.0b1',
      description='Growtopia Unofficial API (WIP)',
	  long_description=README,
	  include_package_data=True,
	  long_description_content_type="text/markdown",
      packages=find_packages(),
	  install_requires=["requests", "pyenet"],
      author='HanzHaxors',
	  author_email="hanzhaxors@gmail.com",
	  license='MIT',
      zip_safe=False)
