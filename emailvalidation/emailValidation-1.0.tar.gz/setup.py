from setuptools import setup

setup(
    name='emailValidation',
    version='1.0',
    packages=['emailValidation'],
    url='https://github.com/UmadeviJ/emailValidation.git',
    license='MIT',
    author='uma',
    author_email='uma.omnn@gmail.com',
    download_url="https://github.com/UmadeviJ/emailValidation/archive/1.0.tar.gz",
    description='To Verify email',
    install_requires=[            # I get to this in a second
          'validators',
          'beautifulsoup4',
      ]
)
