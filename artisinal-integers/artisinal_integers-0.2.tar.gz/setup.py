from setuptools import setup

setup(name='artisinal_integers',
      version='0.2',
      description='get a unique artisinal integer',
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
