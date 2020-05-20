from setuptools import setup, find_packages

def readme ():
    with open('README.md') as me:
        return me.read()

setup(name='thc',
      version='0.2.1',
      description='Trustable homomorphic computation',
      long_description=readme(),
      long_description_content_type='text/markdown',
      url='https://pablo.rauzy.name/software.html#thc',
      author='Pablo Rauzy',
      author_email='pr_NOSPAM'+chr(64)+'up8.edu',
      license='GNU AGPL v3+',
      packages=find_packages(),
      include_package_data=True,
      install_requires=[
          'pycrypto'
      ],
      extras_require={
          'evoting': [
              'PyNaCl',
              'requests'
          ]
      },
      entry_points={
          'console_scripts': [
              'thc_evoting-client = thc.demo.evoting.client:main [evoting]',
              'thc_evoting-server = thc.demo.evoting.server:main [evoting]'
          ]
      })
