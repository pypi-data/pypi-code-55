from setuptools import setup, find_packages

setup(
      name='methinks',
      packages=find_packages(),
      include_package_data=True,
      version='0.0.2',
      author='Andreas Grivas',
      author_email='andreasgrv@gmail.com',
      description='Keep track of your reading, your todos and your notes. Whatever thinketh you.',
      download_url = 'https://github.com/andreasgrv/methinks/archive/0.0.2.tar.gz',
      license='BSD',
      keywords=['self reporting'],
      scripts=['bin/today',
               'bin/today-python',
               'bin/methinks-env'
               ],
      install_requires=['flask-sqlalchemy>=2.0',
                        'markdown>=3.0',
                        'pyyaml>=5.1.2',
                        'requests>=2.20',
                        'xxhash>=1.4'],
      classifiers=[],
      python_requires='>=3.6',
      tests_require=['pytest'],
)
